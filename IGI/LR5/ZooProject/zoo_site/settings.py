import os
from pathlib import Path
import dj_database_url

# Путь к папке проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# БЕЗОПАСНОСТЬ: В Docker/на сервере берем ключ из переменных окружения, иначе используем дефолт
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-default-key-keep-it-safe')

# DEBUG будет True только если переменная окружения DEBUG=True, иначе False (для деплоя)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Разрешаем все хосты для Docker и Render
ALLOWED_HOSTS = ['*']

TIME_ZONE = 'Europe/Minsk'
USE_I18N = True
USE_TZ = True

SUPPORTED_TIMEZONES = [
    'Europe/Minsk',
    'Europe/Moscow',
    'Europe/Kiev',
    'Europe/London',
    'America/New_York',
    'Asia/Tokyo',
]
# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'animals',  # Твое приложение
]

# Порядок Middleware критически важен для работы админки и статики
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Сжатие и кэширование статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'animals.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'zoo_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },

    },
]

WSGI_APPLICATION = 'zoo_site.wsgi.application'

# --- БАЗА ДАННЫХ ---
# Если переменная DATABASE_URL есть (Docker/Render) - используем её, иначе SQLite
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600
    )
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'

# --- СТАТИКА И МЕДИА ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise для раздачи статики в Docker без Nginx
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SERVER_NAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'Локальный сервер (разработка)')
SERVER_TYPE = os.environ.get('SERVER_TYPE', 'Локальный сервер')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# --- ЛОГИРОВАНИЕ ---
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'animals': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        }
    },
}