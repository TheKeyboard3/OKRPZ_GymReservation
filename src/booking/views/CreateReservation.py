import logging
from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import datetime, timedelta
from django.views.generic import FormView
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

        yesterday = datetime.today()
        selected_date = self.request.GET.get('date',
                                             yesterday.strftime('%Y-%m-%d'))
        try:
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            raise Http404('Некоректний формат дати')

        trainer = TrainerProfile.objects.select_related(
            'user').get(user__id=self.kwargs['id'])

        # Генеруємо список днів для розкладу
        schedule_days = [(yesterday.date() + timedelta(days=i))
                         for i in range(3*7)]

        # Отримуємо всі графіки тренера для обраного періоду одним запитом
        all_work_schedules = WorkSchedule.objects.filter(
            trainer=trainer,
            start_time__date__range=(schedule_days[0], schedule_days[-1])
        ).order_by('start_time')

        # Розподіляємо графіки за днями
        schedule_by_day = {day: [] for day in schedule_days}

        for schedule in all_work_schedules:
            schedule_date = schedule.start_time.date()

            if schedule_date in schedule_by_day:
                schedule_by_day[schedule_date].append(schedule)

        # Отримуємо графік роботи тренера на обраний день
        daily_work_schedules = schedule_by_day.get(selected_date.date(), [])

        if not daily_work_schedules:
            context['available_slots'] = []
            context['error'] = 'У цей день тренер не працює'
            context['selected_date'] = selected_date.strftime('%Y-%m-%d')
            context['trainer'] = trainer
            context['schedule_days'] = schedule_days
            context['schedule_by_day'] = schedule_by_day
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

        for schedule in daily_work_schedules:
            current_slot = schedule.start_time

            while current_slot + timedelta(hours=1) <= schedule.end_time:
                slot_start = current_slot.time()
                slot_end = (current_slot + timedelta(hours=1)).time()

                if not any(
                    reserved_start <= slot_start < reserved_end or
                    reserved_start < slot_end <= reserved_end
                    for reserved_start, reserved_end in reserved_slots
                ):
                    available_slots.append(
                        f"{slot_start.strftime('%H:%M')} - {slot_end.strftime('%H:%M')}"
                    )

                current_slot += timedelta(hours=1)

        # Передаємо дані в контекст
        context['selected_date'] = selected_date.strftime('%Y-%m-%d')
        context['trainer'] = trainer
        context['schedule_days'] = schedule_days
        context['schedule_by_day'] = schedule_by_day
        context['work_schedule'] = daily_work_schedules
        context['available_slots'] = available_slots

        return context

    def form_valid(self, form):
        try:
            trainer = TrainerProfile.objects.select_related(
                'user').get(user__id=self.kwargs['id'])
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
