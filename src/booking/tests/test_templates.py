from django.test import TestCase
from booking.models import Departament, Reservation
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

        self.tp1 = TrainerProfile.objects.create(
            user=self.tr1,
            bio='Опис тренера та його види зайнятості',
            phone_number='+380680382525')

        self.tr2 = User.objects.create_user(
            username='3',
            first_name='Назар',
            last_name='Боднар',
            email='bodnar@gmail.com',
            password='123456',
            is_active=True)

        self.tp2 = TrainerProfile.objects.create(
            user=self.tr2,
            bio='Опис',
            phone_number='+380680382525')

        self.client1 = User.objects.create_user(
            username='4',
            first_name='Віктор',
            last_name='Вуйко',
            email='vuico@gmail.com',
            password='123456',
            is_active=True)

        self.cp1 = ClientProfile.objects.create(
            user=self.client1)

        self.client2 = User.objects.create_user(
            username='5',
            first_name='Клієнт',
            last_name='№2',
            email='client2@gmail.com',
            password='123456',
            is_active=True)

        self.cp2 = ClientProfile.objects.create(
            user=self.client2)

        self.dep1 = Departament.objects.create(
            title='Басейн')

        self.reservation1 = Reservation.objects.create(
            trainer=self.tp1,
            client=self.cp1,
            departament=self.dep1,
            start_date='2024-11-30 10:00',
            end_date='2024-11-30 11:00',
        )

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

    def test_create_reservation_if_admin(self):
        login = self.client.login(email='admin1@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.get(f'/trainers/{self.tr1.pk}/reservation')

        self.assertEqual(response.status_code, 200)

    def test_create_reservation_if_trainer(self):
        login = self.client.login(email='bodnar@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.get(f'/trainers/{self.tr1.pk}/reservation')

        self.assertEqual(response.status_code, 403)

    def test_create_reservation_if_client(self):
        login = self.client.login(email='vuico@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.get(f'/trainers/{self.tr1.pk}/reservation')

        self.assertEqual(response.status_code, 200)

    def test_reservation_delete_if_different_client(self):
        login = self.client.login(email='client2@gmail.com', password='123456')
        self.assertTrue(login)
        response = self.client.post(
            f'reservation/{self.reservation1.pk}/delete')

        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            Reservation.objects.filter(pk=self.reservation1.pk).exists())
