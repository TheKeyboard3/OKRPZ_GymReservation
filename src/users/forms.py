from django.forms import Form, ModelForm, CharField, EmailField, ImageField, ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django_recaptcha.fields import ReCaptchaField
from phonenumber_field.formfields import PhoneNumberField
from users.models import User, ClientProfile, TrainerProfile


class UserLoginForm(AuthenticationForm):
    username = CharField(required=True)
    password = CharField(required=True)


class UserEditForm(UserChangeForm):
    first_name = CharField(required=True)
    last_name = CharField(required=True)
    email = EmailField(disabled=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class ClientProfileEditForm(ModelForm):
    avatar = ImageField(required=False)

    class Meta:
        model = ClientProfile
        fields = ('avatar',)


class TrainerProfileEditForm(ModelForm):
    avatar = ImageField(required=False)
    phone_number = PhoneNumberField(required=True)
    bio = CharField(required=True)

    class Meta:
        model = TrainerProfile
        fields = ('avatar', 'phone_number', 'bio')


class ResetPasswordForm(Form):
    email = EmailField()
    captcha = ReCaptchaField()


class SetNewPasswordForm(Form):
    password1 = CharField()
    password2 = CharField()
    captcha = ReCaptchaField()

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        try:
            validate_password(password1)
        except ValidationError as er:
            self.add_error('password1', er)
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data['password1']
        password2 = cleaned_data['password2']

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Паролі не співпадають')

        return cleaned_data
