from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from django.views.generic import DetailView
from django.views import View
from users.models import TrainerProfile
from booking.models import Reservation


class DeleteReservationView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        reservation = get_object_or_404(Reservation, id=self.kwargs['id'])

        if getattr(self.request.user, 'trainer_profile', False):
            raise Http404('Тренери не можуть видаляти резервації!')

        if reservation.user != self.request.user:
            raise Http404(
                'Ви не можете видаляти резервації інших клієнтів!')

        reservation.delete()
        messages.success(self.request, 'Резервацію успішно видалено')
        return redirect(request.META.get('HTTP_REFERER', '/'))


class TrainersListView(View):

    def get(self, request):
        trainers = TrainerProfile.objects.all().select_related('user')
        context = {
            'trainers': trainers
        }
        return render(request, 'booking/trainers_list.html', context)


class TrainerDetailView(DetailView):

    def get(self, request, id):
        trainer = get_object_or_404(TrainerProfile, user__id=id)

        context = {
            'title': trainer.user.username,
            'trainer': trainer,
        }
        return render(request, 'booking/trainer_detail.html', context)
