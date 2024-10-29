from datetime import time
from django.db.models import Model, CASCADE, PositiveSmallIntegerField, CharField, BooleanField, DateTimeField, TimeField, ForeignKey, IntegerChoices, UniqueConstraint
from users.models import User, ClientProfile, TrainerProfile


class Departament(Model):
    """Відділення спортзалу."""

    title = CharField('Назва відділення', max_length=250)

    class Meta():
        db_table = 'departament'
        verbose_name = 'Відділення спортзалу'
        verbose_name_plural = 'Відділення спортзалу'
        ordering = ['title']

    def __str__(self):
        return self.title


class Reservation(Model):
    """Резервація часу у тренера."""

    client = ForeignKey(ClientProfile, CASCADE, related_name='user_reservations',
                        verbose_name='Клієнт')
    trainer = ForeignKey(TrainerProfile, CASCADE, related_name='trainer_reservations',
                         verbose_name='Тренер')
    departament = ForeignKey(Departament, CASCADE, related_name='reservations',
                            verbose_name='Відділення')

    start_date = DateTimeField('Від')
    end_date = DateTimeField('До')
    active = BooleanField('Чи активна', default=True)
    created = DateTimeField('Дата створення', auto_now=True)

    class Meta():
        db_table = 'reservations'
        verbose_name = 'Резервація часу'
        verbose_name_plural = 'Резервації часу'
        ordering = ['start_date']

    def __str__(self):
        return f'{self.client.user.get_full_name()} забронював час у {self.trainer.user.get_full_name()}'

    def duration_in_hours(self):
        duration = self.end_date - self.start_date
        return round(duration.total_seconds() // 3600)

    def duration_in_minutes(self):
        duration = self.end_date - self.start_date
        return round(duration.total_seconds() // 60)


class WorkSchedule(Model):
    """Графік роботи за день неділі у тренера."""

    class DaysOfWeek(IntegerChoices):
        Monday = 0, 'Понеділок'
        Tuesday = 1, 'Вівторок'
        Wednesday = 2, 'Середа'
        Thursday = 3, 'Четвер'
        Friday = 4, 'П\'ятниця'
        Saturday = 5, 'Субота'
        Sunday = 6, 'Неділя'

    trainer = ForeignKey(TrainerProfile, CASCADE,
                         related_name='work_schedules', verbose_name='Тренер')
    day_of_week = PositiveSmallIntegerField('День неділі',
                                            choices=DaysOfWeek.choices, default=DaysOfWeek.Monday)
    start_time = TimeField('Час початку роботи', default=time(9))
    end_time = TimeField('Час завершення роботи', default=time(17))

    class Meta:
        constraints = [UniqueConstraint(
            fields=['trainer', 'day_of_week'],
            name='unique_trainer_day')
        ]
        db_table = 'work_schedules'
        verbose_name = 'Розклад роботи тренера'
        verbose_name_plural = 'Розклад роботи тренерів'
        ordering = ['trainer', 'day_of_week']

    def __str__(self):
        return f'{self.get_day_of_week_display()} {self.start_time} - {self.end_time}'

    def trainer_name(self):
        return self.trainer.user.get_full_name()
    trainer_name.short_description = 'Тренер'
