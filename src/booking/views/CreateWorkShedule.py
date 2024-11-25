import logging
from datetime import date, time
from django.contrib import messages
from django.utils.timezone import datetime, timedelta
from django.urls import reverse
from django.views.generic import FormView
from core.settings.base import WEEKS
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
            trainer = TrainerProfile.objects.select_related(
                'user').get(user__id=form.cleaned_data['trainer_id'])
            start_date: date = form.cleaned_data['start_date']
            end_date: date = form.cleaned_data['end_date']
            weekday: int = form.cleaned_data['weekday']
            start_time: time = form.cleaned_data['start_time']
            end_time: time = form.cleaned_data['end_time']

            current_date: date = start_date
            created_schedules = []

            while current_date <= end_date:
                if current_date.weekday() == weekday:
                    # Перевірка на існуючу резервацію для поточної дати
                    existing_reservation = Reservation.objects.filter(
                        trainer=trainer,
                        start_date__date=current_date
                    ).exists()

                    if existing_reservation:
                        messages.warning(self.request,
                                         f'{current_date.strftime("%d.%m.%Y")} вже є резервації. Розклад на цей день неможна змінювати')
                    else:
                        update_schedule = WorkSchedule.objects.filter(
                            trainer=trainer,
                            start_time__date=current_date).first()

                        if update_schedule:
                            update_schedule.start_time = datetime.combine(
                                current_date, start_time)
                            update_schedule.end_time = datetime.combine(
                                current_date, end_time)
                            update_schedule.save()
                            messages.success(self.request,
                                             f'Розклад на {current_date.day} число оновлено: {start_time}-{end_time}')
                        else:
                            WorkSchedule.objects.create(
                                trainer=trainer,
                                start_time=datetime.combine(
                                    current_date, start_time),
                                end_time=datetime.combine(
                                    current_date, end_time),
                            )
                            created_schedules.append(current_date)
                            messages.success(self.request,
                                             f'Розклад на {current_date.day} число створено: {start_time}-{end_time}')

                current_date += timedelta(days=1)

            if not created_schedules:
                messages.warning(
                    self.request, 'Розклад не створено: проміжок вибраних днів не включає обраний день тижня')

            return super().form_valid(form)

        except TrainerProfile.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує!')
            return self.form_invalid(form)

    def form_invalid(self, form: CreateWorkSheduleForm):
        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        trainer = TrainerProfile.objects.select_related(
            'user').get(user__id=self.kwargs['id'])
        today = datetime.today()
        schedule_days = [(today.date() + timedelta(days=i))
                         for i in range(WEEKS*7)]

        work_schedules = WorkSchedule.objects.filter(
            trainer=trainer,
            start_time__date__range=(schedule_days[0], schedule_days[-1])
        ).order_by('start_time')

        # Групуємо графіки за днями
        schedule_by_day = {day: [] for day in schedule_days}

        for schedule in work_schedules:
            schedule_date = schedule.start_time.date()
            if schedule_date in schedule_by_day:
                schedule_by_day[schedule_date].append(schedule)

        context['trainer'] = trainer
        context['today'] = today.strftime('%Y-%m-%d')
        context['default_end_date'] = (
            today + timedelta(days=(WEEKS+1)*7)).strftime('%Y-%m-%d')
        context['work_schedule'] = work_schedules
        context['schedule_days'] = schedule_days
        context['schedule_by_day'] = schedule_by_day
        return context

    def get_success_url(self):
        return reverse('booking:shedule_add', kwargs={'id': self.kwargs['id']})
