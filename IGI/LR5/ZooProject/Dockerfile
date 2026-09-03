FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей для Postgres и Pillow
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

# Создаём папку для статики
RUN mkdir -p staticfiles

# Собираем статику при сборке
RUN python manage.py collectstatic --noinput

# Запуск: миграции + создание суперпользователя + gunicorn
CMD python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell || true && \
    gunicorn zoo_site.wsgi:application --bind 0.0.0.0:$PORT