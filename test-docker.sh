#!/bin/bash

# Скрипт для проверки и тестирования Docker конфигурации

set -e

echo "🔍 Проверка Docker конфигурации..."

# Проверка Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

if ! docker ps &> /dev/null; then
    echo "❌ Docker daemon не запущен!"
    echo "💡 Запустите Docker Desktop или Docker daemon"
    exit 1
fi

echo "✅ Docker доступен"

# Проверка файлов
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile не найден!"
    exit 1
fi

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml не найден!"
    exit 1
fi

echo "✅ Файлы конфигурации найдены"

# Создание .env если нет
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✅ Создан .env из примера"
    else
        echo "⚠️  .env файл не найден, используем значения по умолчанию"
    fi
fi

# Создание директории data
mkdir -p data
echo "✅ Директория data создана"

# Остановка старых контейнеров
echo "🛑 Останавливаю старые контейнеры (если есть)..."
docker-compose down 2>/dev/null || true

# Сборка образа
echo "🔨 Сборка Docker образа..."
docker-compose build

echo ""
echo "✅ Сборка завершена успешно!"
echo ""
echo "📋 Следующие шаги:"
echo "  1. Запустить бота: docker-compose up -d"
echo "  2. Посмотреть логи: docker-compose logs -f"
echo "  3. Остановить: docker-compose down"
echo ""

