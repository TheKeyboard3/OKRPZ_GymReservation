import random
import platform
import logging
import django
import rest_framework
from django.http import HttpRequest, Http404, HttpResponse, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.db import connection
from django.views import View
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from core.settings.base import APP_NAME, SITE_SUPPORT_EMAIL
from main import tasks
from email_validator import validate_email, EmailNotValidError


logger = logging.getLogger(__name__)


class IndexView(View):

    def get(self, request: HttpRequest):
        return render(request, 'main/index.html')


class AboutView(View):

    def get(self, request: HttpRequest):
        context = {
            'support_email': SITE_SUPPORT_EMAIL,
        }
        return render(request, 'main/about.html', context)


class HostInfoView(GenericAPIView):

    permission_classes = [IsAdminUser]

    def get(self, request: HttpRequest):
        with connection.cursor() as cursor:
            cursor.execute('SELECT sqlite_version()')
            db_version = cursor.fetchone()[0]

        context = {
            'title': 'Host Info',
            'python_v': platform.python_version(),
            'django_v': django.__version__,
            'drf_v': rest_framework.__version__,
            'database_v': db_version,
            'architecture': platform.architecture(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_implem': platform.python_implementation(),
            'python_revision': platform.python_revision(),
            'python_compiler': platform.python_compiler(),
            'python_branch': platform.python_branch(),
        }
        return render(request, 'main/host_info.html', context)


class NotFoundView(View):

    def get(self, request: HttpRequest):
        raise Http404()


class HTMXExamplesView(LoginRequiredMixin, View):

    def get(self, request: HttpRequest):
        dj_version = django.get_version()
        context = {
            'dj_version': dj_version,
        }
        return render(request, 'main/test_functions.html', context)


class SendEmailView(GenericAPIView):

    permission_classes = [IsAdminUser]

    def get(self, request: HttpRequest):
        int = random.randint(1, 100)
        subject = f'(❁´◡`❁) [{int}] {timezone.now().strftime("%H:%M:%S")}'
        to_email = request.GET.get('email')
        html_message = f'<h3>({APP_NAME})</h3><p>Перевірка <b>Celery</b></p>'
        message = str(int)
        try:
            to_email = validate_email(to_email)['email']
        except EmailNotValidError as error:
            return HttpResponse(f'<div class="form-error mb-1">{error}</div>')

        tasks.send_email.delay(
            to=to_email,
            subject=subject,
            html_message=html_message,
            message=message)

        return JsonResponse({'status': 'ok'})
