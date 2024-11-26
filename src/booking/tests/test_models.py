# from django.test import TestCase
# from booking.models import Reservation, TrainerProfile, Departament
# from django.contrib.auth.models import User


# class ReservationModelTest(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username='trainer1', password='password')
#         self.trainer = TrainerProfile.objects.create(user=self.user)
#         self.departament = Departament.objects.create(name='Фітнес-зал')
#         self.reservation = Reservation.objects.create(
#             trainer=self.trainer,
#             client=None,  # Додайте клієнта, якщо є
#             departament=self.departament,
#             start_date='2024-11-30 10:00',
#             end_date='2024-11-30 11:00'
#         )

#     def test_reservation_creation(self):
#         self.assertEqual(str(self.reservation),
#                          'Фітнес-зал: 2024-11-30 10:00 - 11:00')
