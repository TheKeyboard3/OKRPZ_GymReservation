from django.apps import AppConfig


class BookingConfig(AppConfig):
    name = 'booking'
    verbose_name = 'Резервація часу'

    def ready(self):
        import booking.signals
