# from django.test import TestCase
# from booking.forms import CreateReservationForm
# from datetime import datetime


# class CreateReservationFormTest(TestCase):

#     def test_valid_form(self):
#         data = {
#             'trainer_id': 1,
#             'date': datetime.today().date(),
#             'time_slot': '10:00 - 11:00',
#             'departament': 1
#         }
#         form = CreateReservationForm(data)
#         self.assertTrue(form.is_valid())

#     def test_invalid_form(self):
#         data = {'trainer_id': '', 'date': '50-50-2024',
#                 'time_slot': '', 'departament': ''}
#         form = CreateReservationForm(data)
#         self.assertFalse(form.is_valid())
