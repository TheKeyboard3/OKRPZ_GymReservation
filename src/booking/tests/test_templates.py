from django.test import TestCase
from users.models import TrainerProfile, User


class BookingTemplateTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='max',
            first_name='Максим',
            last_name='Березюк',
            email='berez@gmail.com',
            password='password')
        self.trainer = TrainerProfile.objects.create(
            user=self.user,
            bio='Опис тренера та його види зайнятості',
            phone_number='+380680382525'
        )

    def test_booking_detail_template_correct(self):
        response = self.client.get('/trainers/1/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'booking/trainer_detail.html')
        self.assertTemplateUsed(response, '_notifications.html')
        self.assertContains(response,
                            '<title>Максим Березюк - Fitness First</title>', html=True)
        self.assertContains(response, 'Опис тренера та його види зайнятості')

    def test_trainers_page_template_correct(self):
        response = self.client.get('/trainerss')

        self.assertEqual(response.status_code, 404, 
                         'Перевірка доступу неавторизованим користувачем')
