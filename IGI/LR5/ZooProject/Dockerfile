FROM python:3.11-slim

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Установка системных зависимостей для Postgres и Pillow (картинки)
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

RUN python manage.py collectstatic --noinput

CMD python manage.py migrate --noinput && \
    python manage.py createsuperuser --noinput || true && \
    gunicorn zoo_site.wsgi:application --bind 0.0.0.0:8000
