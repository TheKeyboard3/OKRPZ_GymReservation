from datetime import date, time
from django.utils.timezone import datetime, timedelta, localtime, now
from django.forms import Form, Select, IntegerField, ChoiceField, TypedChoiceField, DateTimeInput, DateTimeField, DateField, TimeField, ValidationError, HiddenInput
from core.settings.base import MIN_RESERVATION_TIME, MAX_RESERVATION_TIME
from users.models import User, TrainerProfile
from booking.models import Reservation, Departament, WeekdayEnum


class CreateReservationForm(Form):
    trainer_id = IntegerField(widget=HiddenInput())
    start_date = DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])
    end_date = DateTimeField(input_formats=['%Y-%m-%dT%H:%M'])
    departament_id = ChoiceField()

    def clean_start_date(self):
        start_date = self.cleaned_data['start_date']
        current_time = localtime(now())
        
        if start_date < current_time:
            raise ValidationError("Час початку не може бути в минулому.")
        
        return start_date

    def clean_end_date(self):
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data['end_date']
        
        if start_date and end_date <= start_date:
            raise ValidationError("Час закінчення має бути пізніше за час початку.")
        
        return end_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        trainer_id = cleaned_data.get('trainer_id')
        
        if start_date and end_date and trainer_id:
            # Перевірка на наявність перекриттів з іншими резерваціями
            overlapping_reservations = Reservation.objects.filter(
                trainer__id=trainer_id,
                start_date__lt=end_date,
                end_date__gt=start_date
            )
            if overlapping_reservations.exists():
                raise ValidationError("Цей час вже зайнятий іншим клієнтом.")

        return cleaned_data


class CreateWorkSheduleForm(Form):
    trainer_id = IntegerField(required=True)
    start_date = DateField(required=True, help_text='Дата початку періоду')
    end_date = DateField(required=True, help_text='Дата завершення періоду')
    weekday = TypedChoiceField(
        coerce=int,
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
        weekday: int = cleaned_data.get('weekday')
        start_time: time = cleaned_data.get('start_time')
        end_time: time = cleaned_data.get('end_time')

        if start_date > end_date:
            raise ValidationError(
                'Дата початку не може бути пізніше дати завершення')

        if start_time >= end_time:
            raise ValidationError(
                'Час початку не може бути пізніше або дорівнювати часу завершення')

        if weekday > 6 or weekday < 0:
            raise ValidationError('Неправильний формат тижня')

        try:
            TrainerProfile.objects.get(user__id=trainer_id)
        except TrainerProfile.DoesNotExist:
            raise ValidationError('Обраного тренера не існує')

        return cleaned_data
