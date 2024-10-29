import logging
from django.core.management.utils import get_random_secret_key
from django.views import View
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.template.response import TemplateResponse
from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from api.serializers import UserListSerializer
from users.models import User
from mimesis import Person, Text, Datetime
from mimesis.builtins import UkraineSpecProvider
from email_validator import validate_email, EmailNotValidError

person = Person('uk')
text = Text('uk')
datetime_gen = Datetime('uk')
ua_provider = UkraineSpecProvider()
tab_text1 = text.text(1)
tab_text2 = text.text(2)
tab_text3 = text.text(4)

logger = logging.getLogger(__name__)


class TestHtmxAPIView(View):
    def get(self, request):
        data = {
            'test': 'HTMX',
            'message': 'HTMX Рулить, Test message',
        }
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


class ModalWindowAPIView(View):
    def get(self, request: HttpRequest):
        query = request.GET.get('title')
        context = {
            'modal_title': 'Модальнко вікно',
            'modal_body': 'Тестове модальне вікно з текстом',
        }
        return TemplateResponse(request, '_modal_window.html', context)


class DateTimeAPIView(View):
    """Отримати поточну дату й час користувача."""

    def get(self, request: HttpRequest):
        data = {
            'datetime': timezone.now().strftime('%d/%m/%Y, %H:%M:%S, %Z%z'),
        }
        return JsonResponse(data)


class ServerDateTimeAPIView(View):
    """Отримати поточну дату й час сервера."""

    def get(self, request):
        data = {
            'datetime': timezone.now().strftime('%d/%m/%Y, %H:%M:%S'),
            'server-timezone': str(timezone.get_current_timezone())
        }
        return JsonResponse(data)


class IP_APIView(View):
    """Отримує IP адресс користувача."""

    def get(self, request: HttpRequest):

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        data = {
            "ip": ip
        }
        return JsonResponse(data)


class HtmxTabsAPIView(View):
    """Отримує HTMX вкладку"""

    def get(self, request: HttpRequest, text: str):

        if text == '2':
            txt = tab_text1
        elif text == '3':
            txt = tab_text2
        else:
            txt = tab_text3

        return HttpResponse(f"""
            <div class='form-error'>
                <h4>Вкладка {text}</h4>
                <p>{txt}</p>
            </div>""")


class GenerateKeyAPIView(View):
    """Отримує згенерований секретний ключ."""

    def get(self, request: HttpRequest):
        key = get_random_secret_key()

        return HttpResponse(key)


class DateTimeSecondsAPIView(View):
    """Отримує поточну дату й час сервера."""

    def get(self, request: HttpRequest):

        return Response(timezone.now().second)


class UserListAPIView(GenericAPIView):
    """Отримує всіх користувачів."""

    def get(self, request: HttpRequest):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True)

        return Response(serializer.data)


class CheckUsernameAPIView(View):
    """Перевіряє чи є користувач з таким username"""

    def get(self, request: HttpRequest):
        username = request.GET['username'].strip()

        if username.__len__() == 0:
            return HttpResponse()
        elif username.__len__() < 3:
            return HttpResponse(f"<div id='check-username' class='form-error'>Закоротке ім'я {username.__len__()}</div>")

        if User.objects.filter(username=username).exists():
            data = "<div id='check-username' class='form-error'>Це ім'я зайняте</div>"
        else:
            data = "<div id='check-username' class='form-success'>Ім'я вільне</div>"

        return HttpResponse(data)


class CheckEmailAPIView(View):
    """Перевіряє чи є користувач з таким email"""

    def get(self, request: HttpRequest):
        email = request.GET['email'].strip()

        try:
            email = validate_email(email)['email']
        except EmailNotValidError as error:
            msg = translate_error(str(error))
            return HttpResponse(f'<div class="form-error mb-1">{msg}</div>')

        if User.objects.filter(email=email).exists() and email != '':
            return HttpResponse("<div class='form-error'>Користувач з таким email вже існує</div>")

        return HttpResponse()


def translate_error(error_message: str):
    translations = {
        'There must be something before the @-sign.':
            'Перед знаком @ повинно бути щось.',
        'An email address must have an @-sign.':
            'Адрес email повинен містити знак @.',
        'The part after the @-sign is not valid. It should have a period.':
            'Частина після знака @ недійсна. У нього повинна бути крапка.',
        'The email address is not valid. It must have exactly one @-sign.':
            'Адреса електронної пошти недійсна. Вона повинна мати рівно один символ @.',
        'The email address is not valid ASCII.':
            'Адреса електронної пошти недійсна (не входить в ASCII)',
        'The email address is not valid.':
            'Адреса електронної пошти недійсна.'
    }
    return translations.get(error_message, error_message)
