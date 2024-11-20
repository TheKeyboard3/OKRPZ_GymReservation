from django.http import HttpRequest
from django.contrib.auth.mixins import AccessMixin
from users.models import ClientProfile, TrainerProfile


class AdminOnlyMixin(AccessMixin):
    """Допускає тільки адміністраторів"""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_staff:
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)


class ClientOnlyMixin(AccessMixin):
    """Допускає тільки клієнтів"""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if hasattr(request.user, 'client_profile'):
            return super().dispatch(request, *args, **kwargs)
        
        return self.handle_no_permission()


class TrainerOnlyMixin(AccessMixin):
    """Допускає тільки тренерів"""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if hasattr(request.user, 'trainer_profile'):
            return super().dispatch(request, *args, **kwargs)
        
        return self.handle_no_permission()


class NotTrainerRequiredMixin(AccessMixin):
    """Не допускає тренерів та не авторизованих."""

    def dispatch(self, request: HttpRequest, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if hasattr(request.user, 'trainer_profile'):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
