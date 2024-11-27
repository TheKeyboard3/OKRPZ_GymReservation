from django.http import Http404
from django.urls import reverse
from django.contrib import messages
from django.utils.timezone import datetime, timedelta
from django.views.generic import FormView
from core.settings.base import WEEKS
from users.models import TrainerProfile
from booking.models import Reservation, WorkSchedule
from booking.mixins import NotTrainerRequiredMixin
from booking.forms import CreateReservationForm


class CreateReservationView(NotTrainerRequiredMixin, FormView):
    template_name = 'booking/create_reservation.html'
    form_class = CreateReservationForm

    def get_selected_date(self):
        """Отримуємо та перевіряємо вибрану дату."""
        yesterday = datetime.today()
        selected_date = self.request.GET.get(
            'date', yesterday.strftime('%Y-%m-%d'))
        try:
            return datetime.strptime(selected_date, '%Y-%m-%d')
        except ValueError:
            raise Http404('Некоректний формат дати')

    def get_trainer(self):
        """Отримуємо тренера за його ID."""
        try:
            return TrainerProfile.objects.select_related('user').get(user__id=self.kwargs['id'])
        except TrainerProfile.DoesNotExist:
            raise Http404('Тренера не знайдено')

    def get_available_departaments(self):
        """Отримуємо доступні департаменти для тренера."""
        trainer = self.get_trainer()
        return trainer.departaments.all()

    def get_schedule_data(self, trainer):
        """Отримуємо всі графіки роботи тренера за обраний період."""
        yesterday = datetime.today()
        schedule_days = [(yesterday.date() + timedelta(days=i))
                         for i in range(WEEKS * 7)]

        all_work_schedules = WorkSchedule.objects.filter(
            trainer=trainer,
            start_time__date__range=(schedule_days[0], schedule_days[-1])
        ).order_by('start_time')

        schedule_by_day = {day: [] for day in schedule_days}
        for schedule in all_work_schedules:
            schedule_date = schedule.start_time.date()
            if schedule_date in schedule_by_day:
                schedule_by_day[schedule_date].append(schedule)

        return schedule_days, schedule_by_day

    def get_reserved_slots(self, trainer, selected_date):
        """Отримуємо всі зайняті слоти тренера на вибрану дату."""
        reservations = Reservation.objects.filter(
            trainer=trainer,
            start_date__date=selected_date
        )
        return {
            (reservation.start_date.time(), reservation.end_date.time())
            for reservation in reservations
        }

    def get_available_slots(self):
        """Генеруємо доступні слоти для вибраного дня."""
        selected_date = self.get_selected_date()
        trainer = self.get_trainer()
        _, schedule_by_day = self.get_schedule_data(trainer)

        daily_work_schedules = schedule_by_day.get(selected_date.date(), [])
        if not daily_work_schedules:
            return []

        reserved_slots = self.get_reserved_slots(trainer, selected_date)

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

        return available_slots

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        selected_date = self.get_selected_date()
        trainer = self.get_trainer()
        user_reservations = Reservation.objects.filter(
            client=self.request.user.profile, 
            trainer=trainer,
            start_date__gt=datetime.now())
        context['user_reservations'] = user_reservations

        schedule_days, schedule_by_day = self.get_schedule_data(trainer)

        daily_work_schedules = schedule_by_day.get(selected_date.date(), [])

        if not daily_work_schedules:
            context.update({
                'available_slots': [],
                'error': 'У цей день тренер не працює',
                'selected_date': selected_date.strftime('%Y-%m-%d'),
                'trainer': trainer,
                'schedule_days': schedule_days,
                'schedule_by_day': schedule_by_day,
            })
            return context

        context.update({
            'selected_date': selected_date.strftime('%Y-%m-%d'),
            'trainer': trainer,
            'schedule_days': schedule_days,
            'schedule_by_day': schedule_by_day,
            'work_schedule': daily_work_schedules,
            'available_slots': self.get_available_slots(),
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        trainer = self.get_trainer()  # Отримуємо тренера
        available_slots = self.get_available_slots()  # Додаємо доступні слоти
        # Додаємо доступні департаменти для тренера
        available_departaments = trainer.departaments.all()
        kwargs['available_slots'] = available_slots  # Додаємо доступні слоти
        # Додаємо департаменти
        kwargs['available_departaments'] = available_departaments
        return kwargs

    def form_valid(self, form):
        """Обробка форми після успішної валідації."""
        trainer = self.get_trainer()
        client = self.request.user.profile
        time_slot = form.cleaned_data['time_slot']
        departament = form.cleaned_data['departament']

        if departament not in trainer.departaments.all():
            form.add_error(
                'departament', 'Вибраний департамент не належить цьому тренеру.')
            return self.form_invalid(form)

        # Розбираємо часовий слот
        start_time, end_time = map(str.strip, time_slot.split(' - '))
        start_datetime = datetime.combine(
            form.cleaned_data['date'],
            datetime.strptime(start_time, '%H:%M').time()
        )
        end_datetime = datetime.combine(
            form.cleaned_data['date'],
            datetime.strptime(end_time, '%H:%M').time()
        )

        # Створюємо резервацію
        Reservation.objects.create(
            client=client,
            trainer=trainer,
            start_date=start_datetime,
            end_date=end_datetime,
            departament=departament
        )

        messages.success(self.request, 'Резервацію створено успішно!')
        return super().form_valid(form)

    def form_invalid(self, form: CreateReservationForm):
        messages.error(self.request, 'Щось пішло не так!')
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER', '/')
