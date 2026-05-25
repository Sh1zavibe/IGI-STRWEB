# animals/context_processors.py

from django.conf import settings

def timezones(request):
    return {'SUPPORTED_TIMEZONES': settings.SUPPORTED_TIMEZONES}