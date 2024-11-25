from datetime import date, time
from django.forms import Form, Select, IntegerField, ChoiceField, ModelChoiceField, TypedChoiceField, DateField, TimeField, ValidationError
from users.models import TrainerProfile
from booking.models import Departament, WeekdayEnum


class CreateReservationForm(Form):
    trainer_id = IntegerField(required=True)
    date = DateField(required=True)
    time_slot = ChoiceField(required=True)
    departament = ModelChoiceField(
        queryset=Departament.objects.none(),
        required=True
    )

    def __init__(self, *args, **kwargs):
        available_slots = kwargs.pop('available_slots', [])
        available_departaments = kwargs.pop('available_departaments',
                                            Departament.objects.none())
        super().__init__(*args, **kwargs)

        self.fields['time_slot'].choices = [
            (slot, slot) for slot in available_slots]
        self.fields['departament'].queryset = available_departaments


class CreateWorkSheduleForm(Form):
    trainer_id = IntegerField(required=True)
    start_date = DateField(required=True)
    end_date = DateField(required=True)
    weekday = TypedChoiceField(
        coerce=int,
        choices=WeekdayEnum.choices(),
        widget=Select(attrs={'class': 'form-control'}),
        required=True
    )
    start_time = TimeField(required=True)
    end_time = TimeField(required=True)

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
