from datetime import date, time
from django.utils.timezone import datetime, timedelta, localtime, now
from django.forms import Form, Select, IntegerField, ChoiceField, DateTimeField, DateField, TimeField, ValidationError
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import User, TrainerProfile
from booking.models import WeekdayEnum


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
            if start_date <= localtime(now()):
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


class CreateWorkSheduleForm(Form):
    trainer_id = IntegerField(required=True)
    start_date = DateField(required=True, help_text='Дата початку періоду')
    end_date = DateField(required=True, help_text='Дата завершення періоду')
    weekday = ChoiceField(
            choices=WeekdayEnum.choices(),
            widget=Select(attrs={'class': 'form-control'}),
            required=True
        )
    start_time = TimeField(required=True, help_text='Час початку роботи')
    end_time = TimeField(required=True, help_text='Час завершення роботи')

    def clean(self):
        cleaned_data = super().clean()

        trainer_id: int = cleaned_data.get('trainer_id')
        start_date: date = cleaned_data.get('start_date')
        end_date: date = cleaned_data.get('end_date')
        start_time: time = cleaned_data.get('start_time')
        end_time: time = cleaned_data.get('end_time')

        if start_date > end_date:
            raise ValidationError(
                'Дата початку не може бути пізніше дати завершення')

        if start_time >= end_time:
            raise ValidationError(
                'Час початку не може бути пізніше або дорівнювати часу завершення')

        try:
            TrainerProfile.objects.get(user__id=trainer_id)
        except TrainerProfile.DoesNotExist:
            raise ValidationError('Обраного тренера не існує')

        return cleaned_data
