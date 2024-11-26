from django.test import TestCase
from users.models import User, ClientProfile, TrainerProfile


class BookingTemplateTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='1',
            first_name='Адміністратор',
            last_name='Вадим',
            email='admin1@gmail.com',
            password='123456',
            is_active=True,
            is_staff=True)
        
        self.tr1 = User.objects.create_user(
            username='2',
            first_name='Максим',
            last_name='Березюк',
            email='berez@gmail.com',
            password='123456',
            is_active=True)

        TrainerProfile.objects.create(
            user=self.tr1,
            avatar=None,
            bio='Опис тренера та його види зайнятості',
            phone_number='+380680382525')

        self.tr2 = User.objects.create_user(
            username='3',
            first_name='Назар',
            last_name='Боднар',
            email='bodnar@gmail.com',
            password='123456',
            is_active=True)

        TrainerProfile.objects.create(
            user=self.tr2,
            avatar=None,
            bio='Опис',
            phone_number='+380680382525')

        self.client1 = User.objects.create_user(
            username='4',
            first_name='Віктор',
            last_name='Вуйко',
            email='vuico@gmail.com',
            password='123456',
            is_active=True)

        ClientProfile.objects.create(
            user=self.client1,
            avatar=None)

    def test_booking_detail_without_login(self):
        response = self.client.get(f'/trainers/{self.tr1.pk}/')

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
        self.assertTemplateUsed(response, 'booking/trainer_detail.html')
        self.assertTemplateUsed(response, '_notifications.html')
        self.assertContains(response,
                            '<title>Максим Березюк - Fitness First</title>', html=True)
        self.assertContains(response, 'Опис тренера та його види зайнятості')

    def test_trainers_list_without_login(self):
        response = self.client.get('/trainers/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Максим Березюк')
        self.assertContains(response, 'Назар Боднар')

    def test_create_work_schedule_if_admin(self):
        login = self.client.login(email='admin1@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.get(f'/trainers/{self.tr1.pk}/schedule/add/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Максим Березюк')

    def test_create_work_schedule_if_trainer(self):
        login = self.client.login(email='berez@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.get(f'/trainers/{self.tr1.pk}/schedule/add/')

        self.assertEqual(response.status_code, 403)

    def test_create_work_schedule_if_client(self):
        login = self.client.login(email='vuico@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.get(f'/trainers/{self.tr1.pk}/schedule/add/')

        self.assertEqual(response.status_code, 403)
