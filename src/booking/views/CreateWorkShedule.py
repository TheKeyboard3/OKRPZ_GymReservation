import logging
from datetime import date, time
from django.db import transaction
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
            trainer = TrainerProfile.objects.get(
                user__id=form.cleaned_data['trainer_id'])
            start_date: date = form.cleaned_data['start_date']
            end_date: date = form.cleaned_data['end_date']
            weekday: int = form.cleaned_data['weekday']
            start_time: time = form.cleaned_data['start_time']
            end_time: time = form.cleaned_data['end_time']

            current_date: date = start_date
            created_schedules = []

            while current_date <= end_date:
                if current_date.weekday() == weekday:
                    update_schedule = WorkSchedule.objects.filter(
                        trainer=trainer,
                        start_time__date=current_date).first()

                    if update_schedule:
                        update_schedule.start_time = datetime.combine(current_date, start_time)
                        update_schedule.end_time = datetime.combine(current_date, end_time)
                        update_schedule.save()
                        messages.success(self.request, 
                                        f'Розклад на {current_date.day} число оновлено: {start_time}-{end_time}')
                    else:
                        WorkSchedule.objects.create(
                            trainer=trainer,
                            start_time=datetime.combine(current_date, start_time),
                            end_time=datetime.combine(current_date, end_time),
                        )
                        created_schedules.append(current_date)
                        messages.success(self.request, 
                                        f'Розклад на {current_date.day} число створено: {start_time}-{end_time}')

                current_date += timedelta(days=1)

            if not created_schedules:
                messages.warning(self.request, 'Розклад не створено: проміжок вибраних днів не включає обраний день тижня')

            return super().form_valid(form)

        except TrainerProfile.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує!')
            logger.error("Trainer profile not found.")
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
