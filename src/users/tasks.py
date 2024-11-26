from celery import shared_task
from .models import User


@shared_task()
def clear_user_token(user_id: int):
    try:
        user = User.objects.get(pk=user_id)
        user.activation_key = None
        user.save()
        return 'ok'
    except User.DoesNotExist:
        return 'error'
