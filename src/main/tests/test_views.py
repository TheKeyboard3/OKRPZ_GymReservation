from django.conf import settings
from django.test import TestCase
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.local')
django.setup()


class TestMainViews(TestCase):

    def test_index_page_return_correct_html(self):
        response = self.client.get('')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'main/index.html')
        self.assertTemplateUsed(response, '_notifications.html')
        self.assertContains(response, f'<title>{settings.APP_NAME}</title>', html=True,
                            msg_prefix='Перевірка title сторінки index')

    def test_about_page_return_correct_html(self):
        response = self.client.get('/about')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertContains(response, f'<title>Про нас - {settings.APP_NAME}</title>', html=True,
                            msg_prefix='Перевірка title сторінки about')
