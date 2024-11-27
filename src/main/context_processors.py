from django.utils.timezone import datetime
from django.http import HttpRequest
from django.conf import settings


def base_processors(request: HttpRequest):
    current_year = datetime.now().year

    return {'site_main_title': settings.APP_NAME,
            'admin_path': settings.ADMIN_PATH,
            'current_year': current_year
            }
