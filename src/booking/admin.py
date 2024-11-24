from django.contrib import admin
from main.admin import MyAdmin
from users.models import ClientProfile, TrainerProfile
from booking.models import Departament, Reservation, WorkSchedule, WeekdayEnum


@admin.register(Departament)
class DepartamentAdmin(MyAdmin):
    list_display = ['title']
    readonly_fields = ['id']
    fields = ['title']


@admin.register(Reservation)
class ReservationAdmin(MyAdmin):
    list_display = ['id', 'client', 'trainer', 'start_date', 'end_date',
                    'display_weekday', 'created',]
    list_display_links = ['client']
    list_filter = ['created']
    date_hierarchy = 'created'
    readonly_fields = ['created']
    list_per_page = 20
    fields = [
        ('client', 'trainer', 'created'),
        ('start_date', 'end_date'),
        ('departament')
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

    def display_weekday(self, obj: Reservation):
        for day in WeekdayEnum:
            if day.value[0] == obj.start_date.weekday():
                return day.value[1]
        return '-'
    display_weekday.short_description = 'День тижня'


@admin.register(WorkSchedule)
class WorkScheduleAdmin(MyAdmin):
    list_display = ['trainer_name', 'start_time',
                    'end_time', 'display_weekday']
    list_filter = ['trainer']
    readonly_fields = []
    list_per_page = 20
    fields = [
        'trainer',
        ('start_time', 'end_time')
    ]

    def display_weekday(self, obj: WorkSchedule):
        for day in WeekdayEnum:
            if day.value[0] == obj.start_time.weekday():
                return day.value[1]
        return '-'
    display_weekday.short_description = 'День тижня'
