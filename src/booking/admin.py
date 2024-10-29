from django import forms
from django.contrib import admin
from booking.models import Departament, Reservation, WorkSchedule
from users.models import User, ClientProfile, TrainerProfile


@admin.register(Departament)
class DepartamentAdmin(admin.ModelAdmin):
    list_display = ['title']
    readonly_fields = ['id']
    fields = ['title']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'trainer', 'created',
                    'start_date', 'end_date', 'active']
    list_display_links = ['client']
    list_filter = ['created', 'active']
    date_hierarchy = 'created'
    readonly_fields = ['created', 'active']
    list_per_page = 20
    fields = [
        ('client', 'trainer', 'created'),
        ('start_date', 'end_date'),
        ('departament', 'active')
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':
            kwargs['queryset'] = ClientProfile.objects.all()

        if db_field.name == 'trainer':
            kwargs['queryset'] = TrainerProfile.objects.all()

        if db_field.name == 'departament':
            first = Departament.objects.first()

            if first:
                kwargs['initial'] = first
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class WorkScheduleOverrideForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
        widgets = {
            'start_time': forms.TimeInput(format='%H:%M'),
            'end_time': forms.TimeInput(format='%H:%M'),
        }


@admin.register(WorkSchedule)
class WorkScheduleAdmin(admin.ModelAdmin):
    form = WorkScheduleOverrideForm
    list_display = ['trainer_name', 'day_of_week', 'start_time', 'end_time']
    list_filter = ['trainer']
    readonly_fields = []
    list_per_page = 20
    fields = [
        'trainer',
        'day_of_week',
        ('start_time', 'end_time')
    ]
