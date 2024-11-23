import logging
from datetime import datetime
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.utils.timezone import datetime

from core.settings.base import APP_NAME, EMAIL_HOST_USER
from main.tasks import send_email
from users.models import TrainerProfile
from booking.models import Reservation, WorkSchedule
from booking.mixins import AdminOnlyMixin

logger = logging.getLogger(__name__)


class RemoveWorkSchedule(AdminOnlyMixin, View):
    def get(self, request, id: int, date: str, *args, **kwargs):
        try:
            # Перевірка формату дати
            target_date = datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponseBadRequest('Неправильний формат дати. Очікується YYYY-MM-DD')

        # Отримуємо тренера
        trainer = get_object_or_404(TrainerProfile, user__id=id)

        # Отримуємо всі резервації для цього розкладу
        reservations = Reservation.objects.filter(
            trainer=trainer,
            start_date__date=target_date
        )

        for reservation in reservations:
            send_email(
                to=reservation.client.user.email,
                subject=f'Скасування резервації ({APP_NAME})',
                message=f'Скасування резервації ({APP_NAME})',
                html_message=f"""
                    <h2>Скасування резервації ({APP_NAME})</h2>
                    <p>{reservation.client.user.first_name}, ваша резервація на {reservation.start_date.strftime('%Y-%m-%d %H')} була скасована</p>
                    <p><a href="">Більше на сайті</a></p>"""
            )

        # Видаляємо резервації
        reservations_deleted_count, _ = reservations.delete()

        # Видаляємо розклад
        deleted_count, _ = WorkSchedule.objects.filter(
            trainer=trainer,
            start_time__date=target_date
        ).delete()

        if deleted_count > 0:
            return redirect(reverse('booking:shedule_add', kwargs={'id': id}))

        if reservations_deleted_count > 0:
            return HttpResponseBadRequest('Резервації були видалені, але розклад не знайдено.')
        
        return HttpResponseBadRequest('Розклад для вказаної дати не знайдено')