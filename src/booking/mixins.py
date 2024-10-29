from django.contrib.auth.mixins import AccessMixin
from django.http import HttpRequest


class NotTrainerRequiredMixin(AccessMixin):
    """Не допускає тренерів та не авторизованих."""

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, 'trainer_profile', False):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
