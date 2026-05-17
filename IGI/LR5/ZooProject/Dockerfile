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

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Устанавливаем gunicorn на случай, если его нет в requirements.txt
RUN pip install gunicorn

# Копируем остальной код
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

# Команда запуска:
# 1. Применяем миграции (создаем таблицы)
# 2. Создаем суперпользователя (пропустит, если уже есть)
# 3. Запускаем сервер
CMD python manage.py migrate --noinput && \
    python manage.py createsuperuser --noinput || true && \
    gunicorn zoo_site.wsgi:application --bind 0.0.0.0:8000
