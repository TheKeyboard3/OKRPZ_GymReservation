from django.http import HttpRequest
from django.utils import timezone
from django.conf import settings

from user_agents import parse


def base_processors(request: HttpRequest):
    current_year = timezone.now().year
    user_agent = parse(request.META.get('HTTP_USER_AGENT', ''))

    return {'site_main_title': settings.APP_NAME,
            'admin_path': settings.ADMIN_PATH,
            'current_year': current_year,
            'user_agent': user_agent,
            }
