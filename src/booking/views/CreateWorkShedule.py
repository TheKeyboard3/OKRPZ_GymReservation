import logging
from datetime import date, time
from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, localtime
from django.urls import reverse
from django.views.generic import FormView
from users.models import TrainerProfile
from booking.models import Reservation, WorkSchedule
from booking.forms import CreateWorkSheduleForm
from booking.mixins import AdminOnlyMixin

logger = logging.getLogger(__name__)


class CreateWorkShedule(AdminOnlyMixin, FormView):
    template_name = 'booking/create_work_shedule.html'
    form_class = CreateWorkSheduleForm

    def form_valid(self, form: CreateWorkSheduleForm):
        try:
            trainer = TrainerProfile.objects.get(user__id=form.cleaned_data['trainer_id'])
            start_date: date = form.cleaned_data['start_date']
            end_date: date = form.cleaned_data['end_date']
            weekday: int = form.cleaned_data['weekday']
            start_time: time = form.cleaned_data['start_time']
            end_time: time = form.cleaned_data['end_time']

            # Генерація розкладу для вибраного дня тижня
            current_date: date = start_date
            created_schedules = []

            # Логування початкових значень
            logger.debug(f"Початкова дата: {start_date}, Кінцева дата: {end_date}, День тижня: {weekday}")

            while current_date <= end_date:
                # Лог для перевірки дня тижня
                logger.debug(f"Перевіряю {current_date}, день тижня: {current_date.weekday()}")  # Логування

                if current_date.weekday() == weekday:
                    start_datetime = datetime.combine(current_date, start_time)
                    end_datetime = datetime.combine(current_date, end_time)

                    # Перевірка на конфлікт із існуючими бронюваннями
                    if Reservation.objects.filter(
                        trainer=trainer,
                        start_date__lt=end_datetime,
                        end_date__gt=start_datetime
                    ).exists():
                        messages.error(self.request, f"Неможливо додати розклад на {current_date}: є бронювання.")
                        return self.form_invalid(form)

                    # Створення нового розкладу
                    WorkSchedule.objects.create(
                        trainer=trainer,
                        start_time=start_datetime,
                        end_time=end_datetime,
                    )
                    created_schedules.append(current_date)

                    # Логування додавання розкладу
                    logger.debug(f"Розклад додано для {current_date}")

                # Додаємо наступний день
                current_date += timedelta(days=1)

            if created_schedules:
                messages.success(self.request, f"Розклад успішно створено для {len(created_schedules)} днів.")
            else:
                messages.warning(self.request, "Розклад не створено: жоден день не відповідає обраному дню тижня.")
            
            return super().form_valid(form)

        except TrainerProfile.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує!')
            return self.form_invalid(form)

    def form_invalid(self, form: CreateWorkSheduleForm):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trainer = TrainerProfile.objects.get(user__id=self.kwargs['id'])
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

        context['trainer'] = trainer
        context['current_day'] = current_date.weekday()
        context['work_schedule'] = work_schedules
        context['schedule_days'] = schedule_days
        context['schedule_by_day'] = schedule_by_day
        return context

    def get_success_url(self) -> str:
        return reverse('booking:shedule_add', kwargs={'id': self.kwargs['id']})
