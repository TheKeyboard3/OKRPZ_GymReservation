from django.forms import Form, IntegerField, DateTimeField
from django.utils import timezone
from django.utils.timezone import datetime, timedelta, localtime
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import User


class CreateReservationForm(Form):
    trainer_id = IntegerField(required=True)
    start_date = DateTimeField(required=True)
    end_date = DateTimeField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        trainer = User.objects.filter(
            trainer_profile__isnull=False).get(id=cleaned_data['trainer_id'])
        
        start_date: datetime = cleaned_data.get('start_date')
        end_date: datetime = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date <= localtime(timezone.now()):
                self.add_error(
                    'start_date', '"Час початку" не може бути в минулому!')

            if end_date <= start_date:
                self.add_error('end_date',
                               '"Час кінця" не може бути меншим за час початку резервації!')

            if (end_date - start_date) < timedelta(minutes=MAX_RESERVATION_TIME):
                self.add_error(None,
                               f'Мінімальний час резервації: {MAX_RESERVATION_TIME} хвилин!')

            if start_date.date() != end_date.date():
                self.add_error(None, 'Це має бути в один день!')

            if start_date.minute % 15 != 0:
                self.add_error('start_date',
                               f'Час початку має бути кратним {MAX_RESERVATION_TIME} хвилинам!')

            if end_date.minute % 15 != 0:
                self.add_error('end_date',
                               f'Час кінця має бути кратним {MAX_RESERVATION_TIME} хвилинам!')

        return cleaned_data
