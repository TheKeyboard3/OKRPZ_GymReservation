from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, localtime
from django.urls import reverse
from django.views.generic import FormView
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import TrainerProfile, ClientProfile, User
from booking.models import Departament, Reservation, WorkSchedule
from booking.mixins import NotTrainerRequiredMixin
from booking.forms import CreateReservationForm


class CreateReservationView(FormView):
    template_name = 'booking/create_reservation.html'
    form_class = CreateReservationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_date = localtime(timezone.now())

        # Оновлюємо мінімальний час старту
        if current_date.minute > 0:
            min_start_time = current_date.replace(
                minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            min_start_time = current_date.replace(
                minute=0, second=0, microsecond=0)

        trainer = TrainerProfile.objects.get(user__id=self.kwargs['id'])
        work_schedule = WorkSchedule.objects.filter(trainer=trainer)
        reservations = Reservation.objects.filter(trainer=trainer,
                                                  start_date__gte=current_date).order_by('start_date')

        # Створюємо словник для зберігання існуючих бронювань
        reservation_dict = {}

        for reservation in reservations:
            start_time = reservation.start_date
            end_time = reservation.end_date

            while start_time < end_time:
                reservation_dict[start_time] = True
                start_time += timedelta(minutes=MIN_RESERVATION_TIME)

        # Дні для показу доступних слотів (14 днів наперед)
        schedule_days = [(current_date.date() + timedelta(days=i))
                         for i in range(14)]

        schedule_by_day = {
            day: work_schedule.filter(
                start_time__date=day
            ).order_by('start_time')
            for day in schedule_days
        }

        # Підготовка контексту для шаблону
        context['trainer'] = trainer
        context['schedule_days'] = schedule_days
        context['schedule_by_day'] = schedule_by_day
        context['min_start_time'] = min_start_time.strftime('%Y-%m-%dT%H:%M')
        context['max_start_time'] = (min_start_time + timedelta(minutes=MAX_RESERVATION_TIME)).strftime('%Y-%m-%dT%H:%M')
        return context

    def form_valid(self, form: CreateReservationForm):
        try:
            trainer = TrainerProfile.objects.get(user__id=form.cleaned_data['trainer_id'])
            start_date: datetime = form.cleaned_data['start_date']
            end_date: datetime = form.cleaned_data['end_date']
            departament_id = form.cleaned_data['departament_id']

            overlapping_reservations = Reservation.objects.filter(
                trainer=trainer,
                start_date__lt=end_date,
                end_date__gt=start_date
            )

            if overlapping_reservations.exists():
                messages.error(self.request, 'Цей час вже зайнятий! Виберіть інший')
                return self.form_invalid(form)

            departament = get_object_or_404(Departament, id=departament_id)
            
            if departament not in trainer.departaments.all():
                messages.error(self.request, 'Обраний відділ не підходить для цього тренера')
                return self.form_invalid(form)

            Reservation.objects.create(
                client=self.request.user.profile,
                trainer=trainer,
                start_date=start_date,
                end_date=end_date,
                departament=departament
            )

            messages.success(self.request, f'Ви успішно зарезервували час у тренера {trainer.user.get_full_name()}!')
            return super().form_valid(form)

        except TrainerProfile.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує')
            return self.form_invalid(form)

    def form_invalid(self, form: CreateReservationForm):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('booking:reservation', kwargs={'id': self.kwargs['id']})
