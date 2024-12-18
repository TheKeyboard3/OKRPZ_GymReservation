from django.db.models import Model, BooleanField, CharField, TextField, ImageField, EmailField, OneToOneField, ManyToManyField, CASCADE
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
    """User в системі (Клієнт, Тренер, Адміністратор)."""
    username = CharField('Username', max_length=80, blank=True, null=True)
    first_name = CharField('Ім\'я', max_length=150)
    last_name = CharField('Прізвище', max_length=150)
    email = EmailField('Email', unique=True,
                       help_text='Email через який користувач зможе увійти')
    is_staff = BooleanField('Адміністратор', default=False,
                            help_text='Чи є користувач адміністратором')
    activation_key = CharField('Код', max_length=80, blank=True, null=True,
                               help_text='Код активації або зміни паролю')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']

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
    
    @property
    def profile(self):
        if hasattr(self, 'client_profile'):
            return self.client_profile
        if hasattr(self, 'trainer_profile'):
            return self.trainer_profile
        return None


def client_path(instance: User, filename):
    return f'images/clients/{instance.user.id}/{filename}'


def trainer_path(instance: User, filename):
    return f'images/trainers/{instance.user.id}/{filename}'


class Client(User):
    class Meta:
        proxy = True
        verbose_name = 'Клієнт'
        verbose_name_plural = 'Клієнти'

    def get_absolute_url(self):
        return reverse('user:detail', args=[self.id])


class Trainer(User):
    class Meta:
        proxy = True
        verbose_name = 'Тренер'
        verbose_name_plural = 'Тренери'

    def get_absolute_url(self):
        return reverse('booking:detail', args=[self.id])


class Admin(User):
    class Meta:
        proxy = True
        verbose_name = 'Адміністратор'
        verbose_name_plural = 'Адміністратори'


class ClientProfile(Model):
    """Профіль клієнта."""

    user = OneToOneField(User, on_delete=CASCADE,
                         related_name='client_profile', verbose_name='Профіль клієнта')
    avatar = ImageField('Фото профілю', upload_to=client_path,
                        blank=True, null=True)

    class Meta():
        db_table = 'client_profiles'
        verbose_name = 'Профіль клієнта'
        verbose_name_plural = 'Профілі клієнтів'
        ordering = ['user__date_joined']

    def __str__(self):
        return self.user.get_full_name()

    def get_absolute_url(self):
        return reverse('user:detail', args=[self.user.id])


class TrainerProfile(Model):
    """Профіль тренера."""

    user = OneToOneField(User, on_delete=CASCADE,
                         related_name='trainer_profile', verbose_name='Профіль тренера')
    bio = TextField('Опис', blank=True, null=True)
    phone_number = PhoneNumberField('Номер телефону', region='UA',
                                    blank=True, null=True)
    avatar = ImageField('Фото профілю', upload_to=trainer_path,
                        blank=True, null=True)
    departaments = ManyToManyField('booking.Departament', blank=True,
                                   related_name='trainers',
                                   verbose_name='Відділення у яких працює тренер')

    class Meta():
        db_table = 'trainer_profiles'
        verbose_name = 'Профіль тренера'
        verbose_name_plural = 'Профілі тренерів'
        ordering = ['user__date_joined']

    def __str__(self):
        return self.user.get_full_name()
