from django.forms import PasswordInput
from django.db.models import ImageField
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from image_uploader_widget.widgets import ImageUploaderWidget
from main.services import get_html_image
from main.admin import MyAdmin
from users.models import User, Client, Trainer, Admin, ClientProfile, TrainerProfile


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
    filter_horizontal = ('departaments',)
    fields = [
        'avatar',
        'departaments',
        'bio',
        'phone_number'
    ]
    formfield_overrides = {
        ImageField: {'widget': ImageUploaderWidget}
    }


@admin.register(User)
class UserAdmin(MyAdmin):
    list_display = ['first_name', 'last_name',
                    'email', 'is_active']
    list_display_links = ['first_name']
    filter_horizontal = ['groups', 'user_permissions']
    search_fields = ['first_name',
                     'last_name', 'email']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    readonly_fields = ['id', 'email', 'password',
                       'date_joined', 'last_login', 'is_superuser']
    list_per_page = 20
    fields = [
        ('email', 'password'),
        ('first_name', 'last_name'),
        ('is_staff', 'is_active'),
        ('date_joined', 'last_login')
    ]

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)

        if obj and obj.is_superuser:
            fields = [field for field in fields if field != 'is_staff']
        return fields


class BaseUserAdmin(MyAdmin):
    list_display = ['first_name', 'last_name', 'email', 'is_active']
    list_filter = ['is_active']
    search_fields = ['first_name', 'last_name', 'email']
    readonly_fields = ['last_login', 'date_joined']
    list_per_page = 20
    fields = [
        ('email', 'password'),
        ('first_name', 'last_name'),
        ('is_active'),
        ('date_joined', 'last_login')
    ]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'password':
            kwargs['widget'] = PasswordInput(render_value=True)
        return super().formfield_for_dbfield(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if 'password' in form.cleaned_data and not obj.password.startswith('pbkdf2_'):
            obj.password = make_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


@admin.register(Client)
class ClientAdmin(BaseUserAdmin):
    inlines = [ClientProfileInline]
    list_display = ['display_avatar', 'first_name',
                    'last_name', 'email', 'is_active']
    list_display_links = ['first_name']
    list_select_related = ['client_profile']

    def display_avatar(self, obj):
        if obj.client_profile.avatar and obj.client_profile.avatar.url:
            return format_html(get_html_image(obj.client_profile.avatar.url, obj, 'Профіль'))
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
class TrainerAdmin(BaseUserAdmin):
    inlines = [TrainerProfileInline]
    list_display = ['display_avatar', 'first_name',
                    'last_name', 'email', 'is_active']
    list_display_links = ['first_name']
    list_select_related = ['trainer_profile']

    def display_avatar(self, obj):
        if obj.trainer_profile.avatar and obj.trainer_profile.avatar.url:
            return format_html(get_html_image(obj.trainer_profile.avatar.url, obj, 'Профіль'))
    display_avatar.short_description = ''

    def get_queryset(self, request):
        return super().get_queryset(request).filter(trainer_profile__isnull=False)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not hasattr(obj, 'trainer_profile'):
            TrainerProfile.objects.create(user=obj)

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.trainer_profile.save()


@admin.register(Admin)
class AdminAdmin(BaseUserAdmin):
    fields = [
        ('email', 'password'),
        ('first_name', 'last_name'),
        ('is_staff', 'is_active'),
        ('date_joined', 'last_login')
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).filter(is_staff=True)

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        initial['is_staff'] = True
        return initial
