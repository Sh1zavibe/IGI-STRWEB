FROM python:3.11-slim

# Переменные окружения (новый формат через =)
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

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Собираем статику
RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "zoo_site.wsgi:application", "--bind", "0.0.0.0:8000"]
