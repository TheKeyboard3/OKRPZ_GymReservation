from django.utils import timezone
from django.utils.translation import get_language
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpRequest

from core.settings import base
import user_agents
import logging
from logging import INFO


logging.basicConfig(filename=base.LOG_PATH / 'detail.log', level=INFO)
logger = logging.getLogger()


class PrintRequestInfoMiddleware(MiddlewareMixin):
    """Middleware, що логує багато інформації про запит."""

    def __init__(self, get_response):
        self._get_response = get_response

    def __call__(self, request: HttpRequest):
        ip_address = request.META.get('REMOTE_ADDR')
        user_locale = get_language()
        user_timezone = timezone.get_current_timezone_name()
        user_agent_string = request.META.get('HTTP_USER_AGENT')
        user_agent = user_agents.parse(user_agent_string)
        device_type = 'PC' if user_agent.is_pc else 'Mobile' if user_agent.is_mobile else 'Tablet' if user_agent.is_tablet else 'Other'
        browser_info = f'{user_agent.browser.family} {user_agent.browser.version_string}'
        ip = request.META.get('REMOTE_ADDR')

        logger.info(f' User: {request.user}')
        logger.info(f' IP Address: {ip_address}')
        logger.info(f' Locale: {user_locale}')
        logger.info(f' Timezone: {user_timezone}')
        logger.info(f' Device: {device_type}')
        logger.info(f' Browser: {browser_info}')
        logger.info(f' IP: {ip}')

        if request.user.is_authenticated:
            # profile = Profile.objects.get(user=request.user)
            # profile.more_info['ip'] = ip
            # profile.save()
            pass

        response = self._get_response(request)

        return response
