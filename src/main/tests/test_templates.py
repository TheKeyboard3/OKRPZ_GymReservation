from django.test import TestCase


class TestMainTemplates(TestCase):

    def test_about_page_template_correct(self):
        response = self.client.get('/about')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'main/about.html')
        self.assertTemplateUsed(response, '_notifications.html')
        self.assertContains(response, '<title>Про Fitness First</title>', html=True)
