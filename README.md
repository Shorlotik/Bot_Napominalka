# Telegram Bot-напоминалка

Бот для отправки персональных напоминаний пользователю в будние дни (понедельник-четверг) каждый час с 10:00 до 18:00 по времени Минска.

## Быстрый старт

```bash
# 1. Скопируйте пример .env
cp .env.example .env

# 2. Отредактируйте .env (при необходимости)

# 3. Проверьте и соберите Docker образ
./test-docker.sh

# 4. Запустите через Docker
docker-compose up -d

# 5. Смотрите логи
docker-compose logs -f
```

Или используйте Makefile:
```bash
make build  # Сборка образа
make up     # Запуск
make logs   # Логи
make down   # Остановка
```

## Установка и запуск

### Вариант 1: Запуск через Docker (рекомендуется)

1. Убедитесь, что у вас установлены Docker и Docker Compose

2. Запустите скрипт проверки и сборки:
```bash
./test-docker.sh
```

3. Запустите бота:
```bash
docker-compose up -d
```

4. Просмотр логов:
```bash
docker-compose logs -f
```

5. Остановка бота:
```bash
docker-compose down
```

### Вариант 2: Запуск локально

1. Клонируйте репозиторий или скачайте файлы проекта

2. Создайте виртуальное окружение:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

5. Отредактируйте `.env` и укажите ваш токен бота (если отличается от примера)

6. Запустите бота:
```bash
python bot.py
```

## Развертывание на Debian сервере

1. Установите Docker и Docker Compose на сервере:
```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
```

2. Скопируйте проект на сервер (через git, scp или другой способ)

3. Создайте `.env` файл с необходимыми параметрами

4. Запустите бота:
```bash
docker-compose up -d
```

5. (Опционально) Для автозапуска при перезагрузке сервера, создайте systemd сервис:
```bash
# Скопируйте пример файла
sudo cp reminder-bot.service.example /etc/systemd/system/reminder-bot.service

# Отредактируйте путь к проекту
sudo nano /etc/systemd/system/reminder-bot.service
# Замените /path/to/Bot_Napominalka на реальный путь к проекту

# Включите автозапуск
sudo systemctl enable reminder-bot.service
sudo systemctl start reminder-bot.service
```

**Альтернатива:** Используйте скрипт развертывания:
```bash
./deploy.sh
```

## Структура данных

База данных сохраняется в директории `./data/` для сохранности данных при перезапуске контейнера.

## Функциональность

- Автоматическая отправка уникальных сообщений в будние дни каждый час
- Учет праздничных дней Беларуси
- Управление напоминалкой через кнопки (включить/выключить)
- Админ-панель для управления сообщениями и настройками

## Команды для пользователя

- `/start` - Начать работу с ботом

## Команды для админа

- `/admin` - Показать меню админ-команд
- `/add_message <текст>` - Добавить новое сообщение
- `/list_messages` - Показать список всех сообщений
- `/delete_message <id>` - Удалить сообщение
- `/start_reminder` - Запустить напоминалку глобально
- `/stop_reminder` - Остановить напоминалку глобально
- `/stats` - Показать статистику работы бота
- `/set_schedule <start_hour> <end_hour>` - Изменить расписание
