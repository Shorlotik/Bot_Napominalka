#!/bin/bash

# Скрипт для развертывания бота на сервере Debian

set -e

echo "🚀 Начало развертывания Telegram Reminder Bot..."

# Проверка наличия Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Устанавливаем..."
    sudo apt update
    sudo apt install -y docker.io docker-compose
    sudo systemctl enable docker
    sudo systemctl start docker
    echo "✅ Docker установлен"
fi

# Проверка наличия .env файла
if [ ! -f .env ]; then
    echo "⚠️  Файл .env не найден. Создаю из примера..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✅ Создан файл .env из примера"
        echo "⚠️  Пожалуйста, отредактируйте .env файл перед запуском!"
    else
        echo "❌ Файл .env.example не найден!"
        exit 1
    fi
fi

# Создание директории для данных
if [ ! -d "data" ]; then
    mkdir -p data
    echo "✅ Создана директория data/"
fi

# Остановка старых контейнеров (если есть)
echo "🛑 Останавливаю старые контейнеры..."
docker-compose down 2>/dev/null || true

# Сборка образа
echo "🔨 Собираю Docker образ..."
docker-compose build

# Запуск контейнера
echo "▶️  Запускаю бота..."
docker-compose up -d

# Проверка статуса
echo "⏳ Ожидание запуска..."
sleep 5

if docker-compose ps | grep -q "Up"; then
    echo "✅ Бот успешно запущен!"
    echo ""
    echo "📋 Полезные команды:"
    echo "  docker-compose logs -f          - Просмотр логов"
    echo "  docker-compose ps               - Статус контейнера"
    echo "  docker-compose restart           - Перезапуск"
    echo "  docker-compose down              - Остановка"
    echo ""
    echo "📊 Просмотр логов:"
    docker-compose logs --tail=20
else
    echo "❌ Ошибка при запуске бота. Проверьте логи:"
    docker-compose logs
    exit 1
fi

