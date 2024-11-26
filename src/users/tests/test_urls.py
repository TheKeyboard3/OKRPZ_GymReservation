from django.test import TestCase
from django.urls import reverse, resolve
from users import views


class TestUsersUrls(TestCase):

    def test_login_url(self):
        url = '/login/'
        self.assertEqual(reverse('users:login'), url)
        self.assertEqual(resolve(url).func.view_class, views.UserLoginView)

    def test_logout_url(self):
        url = '/logout/'
        self.assertEqual(reverse('users:logout'), url)
        self.assertEqual(resolve(url).func.view_class, views.LogoutView)

    def test_password_reset_url(self):
        url = '/reset-request/'
        self.assertEqual(reverse('users:password_reset'), url)
        self.assertEqual(resolve(url).func.view_class, views.PasswordResetView)

    def test_password_reset_confirm_url(self):
        url = '/reset-confirm/sometoken/'
        self.assertEqual(reverse('users:password_reset_confirm',
                                 kwargs={'token': 'sometoken'}), url)
        self.assertEqual(resolve(url).func.view_class,
                         views.PasswordResetConfirmView)

    def test_client_profile_change_url(self):
        url = '/client-change/'
        self.assertEqual(reverse('users:client_profile_change'), url)
        self.assertEqual(resolve(url).func.view_class,
                         views.ClientProfileChangeView)

    def test_trainer_profile_change_url(self):
        url = '/trainer-change/'
        self.assertEqual(reverse('users:trainer_profile_change'), url)
        self.assertEqual(resolve(url).func.view_class,
                         views.TrainerProfileChangeView)

    def test_client_profile_detail_url(self):
        url = '/profile/1/'
        self.assertEqual(reverse('users:detail', kwargs={'id': 1}), url)
        self.assertEqual(resolve(url).func.view_class,
                         views.ClientProfileDetailView)
