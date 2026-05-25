# animals/middleware.py

from django.utils import timezone
from django.conf import settings

class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем часовой пояс из сессии (если есть)
        tzname = request.session.get('django_timezone')
        if tzname and tzname in settings.SUPPORTED_TIMEZONES:
            timezone.activate(tzname)
        else:
            # Если не задан – деактивируем, будет использоваться UTC
            timezone.deactivate()
        return self.get_response(request)