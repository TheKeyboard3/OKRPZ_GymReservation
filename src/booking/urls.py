from django.urls import path
from booking.views import views
from booking.views.CreateReservation import *
from booking.views.CreateWorkShedule import *
from booking.views.RemoveWorkSchedule import *

app_name = 'booking'

urlpatterns = [
    path('trainers/',
         views.TrainersListView.as_view(), name='trainers'),
    path('trainers/<int:id>/',
         views.TrainerDetailView.as_view(), name='detail'),
    path('trainers/<int:id>/reservation',
         CreateReservationView.as_view(), name='reservation'),
    path('trainers/<int:id>/schedule/add/',
         CreateWorkShedule.as_view(), name='shedule_add'),
    path('trainers/<int:id>/schedule/remove/<str:date>/',
        RemoveWorkSchedule.as_view(), name='schedule_remove'),
    path('reservation/<int:id>/delete/',
         views.DeleteReservationView.as_view(), name='reservation_delete'),
]
