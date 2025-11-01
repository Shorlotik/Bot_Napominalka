FROM python:3.11-slim

# Установка рабочей директории
WORKDIR /app

# Установка системных зависимостей (если нужны)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     && rm -rf /var/lib/apt/lists/*

# Копирование requirements.txt и установка зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Создание директории для базы данных
RUN mkdir -p /app/data

# Установка переменных окружения по умолчанию (можно переопределить через docker-compose)
ENV PYTHONUNBUFFERED=1

# Команда запуска
CMD ["python", "bot.py"]

