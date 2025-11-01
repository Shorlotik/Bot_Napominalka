"""Основной файл Telegram бота-напоминалки"""
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from config import BOT_TOKEN
from database import init_database
from handlers.user_handlers import start_command, button_callback
from handlers.admin_handlers import (
    admin_command,
    add_message_command,
    list_messages_command,
    delete_message_command,
    start_reminder_command,
    stop_reminder_command,
    stats_command,
    set_schedule_command,
    help_command
)
from services.scheduler_service import set_bot_application, start_scheduler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция запуска бота"""
    # Инициализация базы данных
    init_database()
    logger.info("База данных инициализирована")
    
    # Создание приложения бота
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Установить application для планировщика
    set_bot_application(application)
    
    # Регистрация обработчиков команд пользователя
    application.add_handler(CommandHandler("start", start_command))
    
    # Регистрация обработчиков кнопок
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Регистрация обработчиков команд админа
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("add_message", add_message_command))
    application.add_handler(CommandHandler("list_messages", list_messages_command))
    application.add_handler(CommandHandler("delete_message", delete_message_command))
    application.add_handler(CommandHandler("start_reminder", start_reminder_command))
    application.add_handler(CommandHandler("stop_reminder", stop_reminder_command))
    application.add_handler(CommandHandler("stats", stats_command))
    application.add_handler(CommandHandler("set_schedule", set_schedule_command))
    application.add_handler(CommandHandler("help", help_command))
    
    # Запуск планировщика в отдельном потоке
    start_scheduler()
    
    # Запуск бота
    logger.info("Бот запущен")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

