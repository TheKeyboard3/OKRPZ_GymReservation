from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest


class NotTrainerRequiredMixin(AccessMixin):
    """Не допускає тренерів та не авторизованих."""

    def dispatch(self, request: HttpRequest, *args, **kwargs):

        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if hasattr(request.user, 'trainer_profile'):
            return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
