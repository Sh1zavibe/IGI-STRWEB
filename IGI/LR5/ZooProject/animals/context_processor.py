from django.conf import settings

def server_info(request):
    return {
        'server_type': settings.SERVER_TYPE,
    }