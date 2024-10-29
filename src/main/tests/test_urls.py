from django.urls import reverse, resolve
from django.test import TestCase

from main.views import IndexView, AboutView


class TestMainUrls(TestCase):

    def test_index_url(self):

        self.assertEqual(reverse('main:index'), '/')
        self.assertEqual(resolve('/').func.view_class, IndexView)

    def test_about_url(self):

        self.assertEqual(reverse('main:about'), '/about')
        self.assertEqual(resolve('/about').func.view_class, AboutView)
