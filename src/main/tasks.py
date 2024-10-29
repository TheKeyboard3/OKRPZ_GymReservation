from django.core.mail import send_mail
from django.core.management import call_command
from django.http import BadHeaderError
from django.conf import settings

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.schedules import crontab
from smtplib import SMTPException, SMTPResponseException

logger = get_task_logger(__name__)


# beat_schedule = {
#     'every': {
#         'task': 'main.tasks.test',
#         'schedule': crontab('*/1'),
#     },
# }

# @periodic_task(run_every=(hour=0, minute=0), name='test')


@shared_task()
def test():
    print('Task test')
    logger.info('Task test')


@shared_task()
def send_email(to: str | list[str],
               subject: str,
               html_message: str,
               message: str,
               from_email: str = settings.EMAIL_HOST_USER):
    try:
        if isinstance(to, str):
            recipient_list = [to]

        elif isinstance(to, list[str]):
            recipient_list = to

        send_mail(
            subject=subject,
            message=message,
            html_message=html_message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False)

        logger.info('Send email success')
        return True

    except (BadHeaderError, SMTPException, SMTPResponseException) as ex:
        logger.error(f'Send email error: {ex}')
        return False
