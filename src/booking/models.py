from django.db.models import Model, CASCADE, CharField, DateTimeField, ForeignKey
from users.models import ClientProfile, TrainerProfile


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
    start_date = DateTimeField('Початок резервації')
    end_date = DateTimeField('Кінець резервації')
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
    """Графік роботи тренера у конкретний день."""

    trainer = ForeignKey(TrainerProfile, CASCADE,
                         related_name='work_schedules', verbose_name='Тренер')
    start_time = DateTimeField('Час початку роботи')
    end_time = DateTimeField('Час завершення роботи')

    class Meta:
        db_table = 'work_schedules'
        verbose_name = 'Розклад роботи тренера'
        verbose_name_plural = 'Розклад роботи тренерів'
        ordering = ['trainer', 'start_time']

    def __str__(self):
        return f'({self.trainer}) {self.start_time} - {self.end_time}'

    def trainer_name(self):
        return self.trainer.user.get_full_name()
    trainer_name.short_description = 'Тренер'
