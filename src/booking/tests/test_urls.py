from django.test import TestCase
from django.urls import reverse, resolve
from booking.views.CreateReservation import CreateReservationView
from booking.views.CreateWorkShedule import CreateWorkShedule
from booking.views.RemoveWorkSchedule import RemoveWorkSchedule
from booking.views import views


class TestBookingUrls(TestCase):

    def test_trainers_list_url(self):
        url = '/trainers/'
        self.assertEqual(reverse('booking:trainers'), url)
        self.assertEqual(resolve(url).func.view_class, views.TrainersListView)

    def test_trainer_detail_url(self):
        url = '/trainers/1/'
        self.assertEqual(reverse('booking:detail', kwargs={'id': 1}), url)
        self.assertEqual(resolve(url).func.view_class, views.TrainerDetailView)

    def test_create_reservation_url(self):
        url = '/trainers/1/reservation'
        self.assertEqual(reverse('booking:reservation', kwargs={'id': 1}), url)
        self.assertEqual(resolve(url).func.view_class, CreateReservationView)

    def test_create_shedule_url(self):
        url = '/trainers/1/schedule/add/'
        self.assertEqual(reverse('booking:shedule_add', kwargs={'id': 1}), url)
        self.assertEqual(resolve(url).func.view_class, CreateWorkShedule)

    def test_schedule_remove_url(self):
        url = '/trainers/1/schedule/remove/2024-11-22/'
        self.assertEqual(reverse('booking:schedule_remove',
                                 kwargs={'id': 1, 'date': '2024-11-22'}), url)
        self.assertEqual(resolve(url).func.view_class, RemoveWorkSchedule)

    def test_reservation_delete_url(self):
        url = '/reservation/3/delete/'
        self.assertEqual(reverse('booking:reservation_delete',
                                 kwargs={'id': 3}), url)
        self.assertEqual(resolve(url).func.view_class,
                         views.DeleteReservationView)
