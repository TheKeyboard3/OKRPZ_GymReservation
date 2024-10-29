from django.utils.html import format_html
from django.db.models import ImageField
from django.contrib import admin
from django.conf import settings
from main import tasks
from main.services import get_html_image
from .models import User, Client, Trainer, Admin, ClientProfile, TrainerProfile
from admin_extra_buttons.api import ExtraButtonsMixin, button, confirm_action, link, view
from admin_extra_buttons.utils import HttpResponseRedirectToReferrer
from image_uploader_widget.widgets import ImageUploaderWidget


class ClientProfileInline(admin.StackedInline):
    model = ClientProfile
    can_delete = False
    fields = ['avatar']
    formfield_overrides = {
        ImageField: {'widget': ImageUploaderWidget}
    }


class TrainerProfileInline(admin.StackedInline):
    model = TrainerProfile
    can_delete = False
    fields = [
        'avatar',
        'phone_number',
        'bio'
    ]
    formfield_overrides = {
        ImageField: {'widget': ImageUploaderWidget}
    }


@admin.register(User)
class UserAdmin(ExtraButtonsMixin, admin.ModelAdmin):
    list_display = ['first_name', 'last_name',
                    'email', 'is_active']
    list_display_links = ['first_name']
    filter_horizontal = ['groups', 'user_permissions']
    search_fields = ['username', 'first_name',
                     'last_name', 'email']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    readonly_fields = ['id', 'email', 'password',
                       'date_joined', 'last_login', 'is_superuser']
    list_per_page = 20
    fields = [
        'username',
        ('first_name', 'last_name'),
        ('email', 'is_active'),
        'is_staff',
        ('last_login', 'date_joined')
    ]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if obj and obj.is_superuser:
            fields = [field for field in fields if field != 'is_staff']
        return fields

    @button(visible=lambda self, request, obj: obj is not None and request.user.is_superuser,
            change_form=True,
            html_attrs={'style': 'background:#13941a'})
    def send_email_to_user(self, request, obj):
        """Відправити лист тільки конкретному користувачу"""
        if obj and obj.email:
            try:
                # Якщо Celery недоступний, використай базову відправку для перевірки
                tasks.send_email.delay(
                    to=obj.email,
                    subject=f'Привіт {obj.username}',
                    html_message=f'Це тестовий лист для {obj.username} з {settings.APP_NAME}',
                    message=settings.APP_NAME
                )
                self.message_user(
                    request, f'Лист успішно надіслано на {obj.email}')
            except Exception as e:
                self.message_user(
                    request, f'Помилка при надсиланні листа: {str(e)}', level='error')
        else:
            self.message_user(
                request, 'Користувач не має електронної пошти або обліковий запис недоступний', level='error')

        return HttpResponseRedirectToReferrer(request)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    inlines = [ClientProfileInline]
    list_display = ['display_avatar', 'first_name',
                    'last_name', 'email', 'is_active']
    list_display_links = ['first_name']
    list_select_related = ['client_profile']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['last_login', 'date_joined']
    list_per_page = 20
    fields = [
        ('password', 'username'),
        ('first_name', 'last_name'),
        ('email', 'is_active'),
        ('last_login', 'date_joined')
    ]

    def display_avatar(self, obj: Client):
        if obj.client_profile.avatar and obj.client_profile.avatar.url:
            return format_html(
                get_html_image(obj.client_profile.avatar.url, obj, 'Профіль'))
    display_avatar.short_description = ''

    def get_queryset(self, request):
        return super().get_queryset(request).filter(client_profile__isnull=False, is_staff=False)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not hasattr(obj, 'client_profile'):
            ClientProfile.objects.create(user=obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.client_profile.save()


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    inlines = [TrainerProfileInline]
    list_display = ['display_avatar', 'first_name',
                    'last_name', 'email', 'is_active']
    list_display_links = ['first_name']
    list_select_related = ['trainer_profile']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['last_login', 'date_joined']
    list_per_page = 20
    fields = [
        ('password', 'username'),
        ('first_name', 'last_name'),
        ('email', 'is_active'),
        ('last_login', 'date_joined')
    ]

    def display_avatar(self, obj: Trainer):
        if obj.trainer_profile.avatar and obj.trainer_profile.avatar.url:
            return format_html(
                get_html_image(obj.trainer_profile.avatar.url, obj, 'Профіль'))
    display_avatar.short_description = ''

    def get_queryset(self, request):
        return super().get_queryset(request).filter(trainer_profile__isnull=False)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not hasattr(obj, 'trainer_profile'):
            ClientProfile.objects.create(user=obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.trainer_profile.save()


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'email']
    list_per_page = 20

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)
