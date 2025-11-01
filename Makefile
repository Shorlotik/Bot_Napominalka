.PHONY: build up down logs restart clean

# Сборка образа
build:
	docker-compose build

# Запуск контейнера
up:
	docker-compose up -d

# Остановка контейнера
down:
	docker-compose down

# Просмотр логов
logs:
	docker-compose logs -f

# Перезапуск
restart:
	docker-compose restart

# Остановка и удаление контейнеров, образов и volumes
clean:
	docker-compose down -v --rmi all

# Выполнение команды в контейнере
exec:
	docker-compose exec reminder-bot bash

