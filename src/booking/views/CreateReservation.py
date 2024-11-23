import logging
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, localtime, now
from django.urls import reverse
from django.views.generic import FormView
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import TrainerProfile, ClientProfile, User
from booking.models import Departament, Reservation, WorkSchedule
from booking.mixins import NotTrainerRequiredMixin
from booking.forms import CreateReservationForm

logger = logging.getLogger(__name__)


class CreateReservationView(NotTrainerRequiredMixin, FormView):
    template_name = 'booking/create_reservation.html'
    form_class = CreateReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_date = datetime.strptime(
            self.request.GET.get('date'), '%Y-%m-%d').date()
        trainer = TrainerProfile.objects.get(user__id=self.kwargs['id'])
        yesterday = datetime.today()
        min_day_value = yesterday.strftime('%Y-%m-%d')

        # Робочий графік тренера на конкретну дату
        work_schedules = WorkSchedule.objects.filter(
            trainer=trainer, start_time__date=selected_date
        ).order_by('start_time')

        if not work_schedules.exists():
            context['available_slots'] = []
            context['error'] = 'У вибраний день тренер не має розкладу.'
            return context

        # Збираємо зайняті слоти
        reservations = Reservation.objects.filter(
            trainer=trainer,
            start_date__date=selected_date
        )
        reserved_slots = {
            (reservation.start_date.time(), reservation.end_date.time())
            for reservation in reservations
        }

        # Генеруємо доступні слоти
        available_slots = []

        for schedule in work_schedules:
            # Починаємо з початку робочого часу
            current_slot = schedule.start_time

            while current_slot + timedelta(hours=1) <= schedule.end_time:
                slot_start = current_slot.time()
                slot_end = (current_slot + timedelta(hours=1)).time()

                # Додаємо слот, якщо він не зайнятий
                if not any(
                    reserved_start <= slot_start < reserved_end or
                    reserved_start < slot_end <= reserved_end
                    for reserved_start, reserved_end in reserved_slots
                ):
                    available_slots.append(
                        f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                    )

                # Переходимо до наступного слота
                current_slot += timedelta(hours=1)

        work_schedules = WorkSchedule.objects.filter(trainer=trainer)
        current_date = localtime(timezone.now())
        schedule_days = [(current_date.date() + timedelta(days=i))
                         for i in range(14)]

        schedule_by_day = {
            day: work_schedules.filter(
                start_time__date=day
            ).order_by('start_time')
            for day in schedule_days
        }

        # Тренер, день, вибраний час
        context['trainer'] = trainer
        context['selected_date'] = selected_date.strftime('%Y-%m-%d')
        context['available_slots'] = available_slots
        context['min_day_value'] = min_day_value
        # Розклад тренера
        context['work_schedule'] = work_schedules
        context['schedule_days'] = schedule_days
        context['schedule_by_day'] = schedule_by_day
        return context

    def form_valid(self, form):
        try:
            trainer = TrainerProfile.objects.get(
                pk=form.cleaned_data['trainer_id'])
            client = self.request.user.profile
            slot_time = form.cleaned_data['time_slot']
            start_time, end_time = map(str.strip, slot_time.split('-'))

            start_datetime = datetime.combine(
                form.cleaned_data['date'],
                datetime.strptime(start_time, '%H:%M').time()
            )
            end_datetime = datetime.combine(
                form.cleaned_data['date'],
                datetime.strptime(end_time, '%H:%M').time()
            )

            Reservation.objects.create(
                client=client,
                trainer=trainer,
                start_date=start_datetime,
                end_date=end_datetime
            )

            messages.success(self.request, 'Резервацію створено успішно!')
            return super().form_valid(form)
        except TrainerProfile.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує!')
            return self.form_invalid(form)

    def form_invalid(self, form: CreateReservationForm):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('booking:reservation', kwargs={'id': self.kwargs['id']})
