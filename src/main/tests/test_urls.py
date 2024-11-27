from django.test import TestCase
from django.urls import reverse, resolve
from main.views import AboutView


class TestMainUrls(TestCase):

    def test_about_url(self):
        self.assertEqual(reverse('main:about'), '/about')
        self.assertEqual(resolve('/about').func.view_class, AboutView)
