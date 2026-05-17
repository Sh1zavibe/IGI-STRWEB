from django.contrib import admin
from django.urls import path, include # Проверь, что include импортирован
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('animals.urls')), # Эта строка отправляет все запросы в приложение animals
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
