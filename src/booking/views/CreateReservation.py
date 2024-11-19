from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, localtime
from django.urls import reverse
from django.views.generic import FormView
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import User, TrainerProfile
from booking.models import Reservation, WorkSchedule
from booking.mixins import NotTrainerRequiredMixin
from booking.forms import CreateReservationForm


class CreateReservationView(NotTrainerRequiredMixin, FormView):
    template_name = 'booking/create_reservation.html'
    form_class = CreateReservationForm

    def form_valid(self, form: CreateReservationForm):
        try:
            trainer = TrainerProfile.objects.get(id=self.kwargs['id'])

            start_date: datetime = form.cleaned_data['start_date']
            end_date: datetime = form.cleaned_data['end_date']

            schedules = WorkSchedule.objects.filter(
                trainer=trainer, day_of_week=start_date.weekday())

            if not schedules.exists():
                messages.error(self.request, 'Тренер не працює у цей день!')
                return self.form_invalid(form)

            schedule = schedules.first()

            if start_date.time() < schedule.start_time or end_date.time() > schedule.end_time:
                messages.error(
                    self.request, 'Час не входить в робочий графік тренера!')
                return self.form_invalid(form)

            overlapping_reservations = Reservation.objects.filter(
                trainer=trainer,
                start_date__lt=end_date,
                end_date__gt=start_date
            )

            if overlapping_reservations.exists():
                messages.error(
                    self.request, 'Цей час не входить в доступний проміжок!')
                return self.form_invalid(form)

            Reservation.objects.create(
                user=self.request.user,
                trainer=trainer,
                start_date=start_date,
                end_date=end_date
            )
            messages.success(self.request,
                             f'Ви зарезервували час у тренера ({trainer.get_full_name()})')
            return super().form_valid(form)

        except User.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує!')
            return self.form_invalid(form)

    def form_invalid(self, form: CreateReservationForm):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_date = localtime(timezone.now())

        if current_date.minute > 0:
            min_start_time = current_date.replace(
                minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            min_start_time = current_date.replace(
                minute=0, second=0, microsecond=0)

        client = getattr(self.request.user, 'client_profile', None)
        trainer = TrainerProfile.objects.get(id=self.kwargs['id'])
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

        available_times = []
        for schedule in work_schedule:
            # Перевіряємо, чи поточний день тижня відповідає робочому графіку тренера
            if current_date.weekday() == schedule.day_of_week:
                start_time = schedule.start_time
                end_time = schedule.end_time

                current_slot = datetime.combine(
                    current_date.date(), start_time)
                end_of_slot = datetime.combine(current_date.date(), end_time)

                # Цикл для перевірки доступності слотів по 15 хвилин
                while current_slot + timedelta(minutes=MIN_RESERVATION_TIME) <= end_of_slot:
                    # Перевіряємо, чи немає перекриттів з існуючими бронюваннями
                    if current_slot not in reservation_dict:
                        # Додаємо доступний слот до списку
                        available_times.append(
                            f'{current_slot.strftime("%H:%M")} - {(current_slot + timedelta(minutes=MIN_RESERVATION_TIME)).strftime("%H:%M")}'
                        )
                    # Переходимо до наступного слоту
                    current_slot += timedelta(minutes=MIN_RESERVATION_TIME)

        user_reservations = Reservation.objects.filter(
            client=client, trainer=trainer)

        max_start_time = current_date
        min_end_time = min_start_time + timedelta(minutes=MIN_RESERVATION_TIME)
        max_end_time = min_start_time + timedelta(minutes=MAX_RESERVATION_TIME)

        context['trainer'] = trainer
        context['available_times'] = available_times
        context['user_reservations'] = user_reservations
        context['current_day'] = current_date.weekday()
        context['min_start_time'] = min_start_time.strftime('%Y-%m-%dT%H:%M')
        context['max_start_time'] = max_start_time.strftime('%Y-%m-%dT%H:%M')
        context['min_end_time'] = min_end_time.strftime('%Y-%m-%dT%H:%M')
        context['max_end_time'] = max_end_time.strftime('%Y-%m-%dT%H:%M')
        return context

    def get_success_url(self):
        return reverse('booking:reservation', kwargs={'id': self.kwargs['id']})
