from django.db.models import Model, BooleanField, CharField, TextField, ImageField, EmailField, OneToOneField, CASCADE
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class UserClientManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(client_profile__isnull=False)


class UserTrainerManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(trainer_profile__isnull=False)


class UserAdminManager(UserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_staff=True)


class User(AbstractUser):
    """User в системі (Користувач, Тренер, Адмін)."""

    email = EmailField('Email', unique=True,
                       help_text='Email через який користувач зареєструвався')
    is_staff = BooleanField('Адміністратор', default=False,
                            help_text='Чи є користувач адміністратором')
    activation_key = CharField('Код', max_length=80, blank=True, null=True)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    clients = UserClientManager()
    trainers = UserTrainerManager()
    admins = UserAdminManager()

    class Meta():
        db_table = 'users'
        verbose_name = 'Користувач'
        verbose_name_plural = 'Усі користувачі'
        ordering = ['date_joined']

    def __str__(self):
        return self.get_full_name()


def avatar_path(instance: User, filename):
    return f'images/users/{instance.user.id}/avatar/{filename}'


class Client(User):
    class Meta:
        proxy = True
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'
    
    def get_absolute_url(self):
        return reverse('user:detail', args=[self.username])


class Trainer(User):
    class Meta:
        proxy = True
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренери'
    
    def get_absolute_url(self):
        return reverse('booking:detail', args=[self.username])


class Admin(User):
    class Meta:
        proxy = True
        verbose_name = 'Адміністратор'
        verbose_name_plural = 'Адміністратори'


class ClientProfile(Model):
    """Профіль клієнта."""
    
    user = OneToOneField(User, on_delete=CASCADE,
                         related_name='client_profile', verbose_name='Профіль клієнта')
    avatar = ImageField('Фото профілю', upload_to=avatar_path,
                        blank=True, null=True)

    class Meta():
        db_table = 'client_profiles'
        verbose_name = 'Профіль клієнта'
        verbose_name_plural = 'Профілі клієнтів'
        ordering = ['user__date_joined']

    def __str__(self):
        return f'Клієнт ({self.user.get_full_name()})'

    def get_absolute_url(self):
        return reverse('user:detail', args=[self.user.username])


class TrainerProfile(Model):
    """Профіль тренера."""
    
    user = OneToOneField(User, on_delete=CASCADE,
                         related_name='trainer_profile', verbose_name='Профіль тренера')
    bio = TextField('Опис', blank=True, null=True)
    phone_number = PhoneNumberField('Номер телефону', region='UA',
                                    blank=True, null=True)
    avatar = ImageField('Фото профілю', upload_to=avatar_path,
                        blank=True, null=True)

    class Meta():
        db_table = 'trainer_profiles'
        verbose_name = 'Профіль тренера'
        verbose_name_plural = 'Профілі тренерів'
        ordering = ['user__date_joined']

    def __str__(self):
        return f'Тренер ({self.user.get_full_name()})'
