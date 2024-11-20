from django.http import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib import auth, messages
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, FormView
from django.views import View
from core.settings.base import APP_NAME, MEDIA_ROOT, TOKEN_LIFETIME
from main.tasks import send_email
from main.services import create_image
from users.tasks import clear_user_token
from .models import User
from .forms import UserEditForm, ClientProfileEditForm, UserLoginForm, ResetTokenForm, ResetPasswordForm, SetNewPasswordForm
from .services import generate_token


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        next_url = self.request.GET.get(
            'next') or self.request.POST.get('next')
        if next_url:
            return next_url

        return reverse('booking:trainers')


class ClientProfileChangeView(LoginRequiredMixin, View):
    template_name = 'users/client_profile_change.html'

    def get(self, request: HttpRequest):
        user_form = UserEditForm(instance=request.user)
        profile_form = ClientProfileEditForm(instance=request.user.profile)

        context = {
            'form': user_form,
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserEditForm(data=request.POST, instance=request.user)
        profile_form = ClientProfileEditForm(data=request.POST,
                                             instance=request.user.profile,
                                             files=request.FILES)

        if form.is_valid() and profile_form.is_valid():
            form.save()
            profile_form.save()
            messages.success(request, 'Дані користувача успішно змінено')

        context = {
            'form': form,
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)


class TrainerProfileChangeView(LoginRequiredMixin, View):
    template_name = 'users/trainer_profile_change.html'

    def get(self, request: HttpRequest):
        return render(request, self.template_name)

    def post(self, request):
        
        return render(request, self.template_name)


class LogoutView(View):

    def get(self, request: HttpRequest):
        next_page = request.GET.get('next', 'main:index')

        if request.user.is_authenticated:
            messages.success(request, 'Ви вийшли з акаунта')
            auth.logout(request)

        return redirect(next_page)


class ResetWaitView(FormView):
    template_name = 'users/reset_wait.html'
    form_class = ResetTokenForm
    token: str

    def form_valid(self, form):
        self.token = form.cleaned_data['token']
        self.success_url = reverse_lazy(
            'user:register_confirm', kwargs={'token': self.token})
        return super().form_valid(form)


class RegisterConfirmView(View):
    def get(self, request: HttpRequest, token):
        try:
            user = User.objects.get(activation_key=token)

        except User.DoesNotExist:
            messages.error(
                request, 'Неправильний код активації або код застарів')
            return redirect('user:reset_wait')

        except Exception:
            messages.error(request, 'Помилка активації')
            return redirect('user:reset_wait')

        user.is_active = True
        user.activation_key = None

        image_path = f'images/users/{user.id}/avatar/{user.username}.png'
        create_image(MEDIA_ROOT / image_path)
        user.profile.avatar = image_path

        user.save()

        auth.login(request, user, 'django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Ви успішно зареєструвались')

        return redirect('user:profile')


class PasswordResetView(FormView):
    template_name = 'users/password_reset.html'
    form_class = ResetPasswordForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form: ResetPasswordForm):
        email = form.cleaned_data['email']
        user = User.objects.filter(email=email).first()

        if user:
            token = generate_token()
            user.activation_key = token
            user.save()
            reset_url = self.request.build_absolute_uri(
                reverse_lazy('user:password_reset_confirm', kwargs={'token': token}))

            send_email.delay(
                to=email,
                subject=f'Відновлення паролю на сайті ({APP_NAME})',
                html_message=f"""
                    <h2>Відновлення паролю на сайті ({APP_NAME})</h2>
                    <p>Щоб відновити пароль перейдіть за посиланням: {reset_url}</p>""",
                message=f'({APP_NAME}) Щоб відновити пароль перейдіть за посиланням: {reset_url}')

            clear_user_token.apply_async((user.pk,), countdown=TOKEN_LIFETIME)

            messages.success(
                self.request, 'Перевірте свою електронну пошту для відновлення паролю.')
        else:
            messages.error(
                self.request, 'Користувача з такою електронною поштою не знайдено.')

        return super().form_valid(form)


class PasswordResetConfirmView(FormView):
    template_name = 'users/password_reset_confirm.html'
    form_class = SetNewPasswordForm
    success_url = reverse_lazy('booking:trainers')

    def get(self, request, *args, **kwargs):
        token = kwargs.get('token')
        user = self.get_user_by_token(token)

        if user is None:
            messages.error(
                self.request, 'Це посилання для зміни пароля застаріло')
            return redirect('users:login')

        return super().get(request, *args, **kwargs)

    def form_valid(self, form: SetNewPasswordForm):
        token = self.kwargs.get('token')
        user = self.get_user_by_token(token)
        if user:
            user.set_password(form.cleaned_data['password1'])
            user.activation_key = None
            user.is_active = True
            user.save()
            messages.success(
                self.request, 'Пароль успішно змінено. Увійдіть з новим паролем.')
        else:
            messages.error(
                self.request, 'Неправильний токен для зміни пароля.')
        return super().form_valid(form)

    def get_user_by_token(self, token):
        try:
            return User.objects.get(activation_key=token)
        except User.DoesNotExist:
            return None


class ProfileDetailView(DetailView):

    def get(self, request: HttpRequest, id):
        user = get_object_or_404(User, id=id)
        context = {
            'title': user.get_full_name(),
            'detail_user': user,
        }
        return render(request, 'users/client_profile.html', context)
