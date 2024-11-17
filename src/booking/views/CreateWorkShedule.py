from django.contrib import messages
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, localtime
from django.urls import reverse
from django.views.generic import FormView
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import User, TrainerProfile
from booking.models import Reservation, WorkSchedule
from booking.mixins import NotTrainerRequiredMixin
from booking.forms import CreateWorkSheduleForm


class CreateWorkShedule(NotTrainerRequiredMixin, FormView):
    template_name = 'booking/create_work_shedule.html'
    form_class = CreateWorkSheduleForm

    def form_valid(self, form: CreateWorkSheduleForm):
        try:
            trainer = TrainerProfile.objects.get(
                user__username=self.kwargs['id'])

            # messages.error(self.request, 'Помилка')
            # return self.form_invalid(form)

            messages.success(self.request, 'Розклад додано')
            return super().form_valid(form)

        except User.DoesNotExist:
            messages.error(self.request, 'Такого тренера не існує!')
            return self.form_invalid(form)

    def form_invalid(self, form: CreateWorkSheduleForm):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self) -> str:
        return reverse('booking:shedule_add', kwargs={'id': self.kwargs['id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_date = localtime(timezone.now())

        trainer = TrainerProfile.objects.get(
            user__id=self.kwargs['id'])
        work_schedule = WorkSchedule.objects.filter(trainer=trainer)

        context['trainer'] = trainer
        context['current_day'] = current_date.weekday()
        return context
