"""Сервис планировщика для отправки сообщений по расписанию"""
import logging
import threading
import time
from datetime import datetime
import schedule
from telegram.error import TelegramError

from config import USER_ID
from models import UserSettings, ScheduleSettings, SentMessage
from services.message_service import get_next_unique_message, mark_message_as_sent
from utils.timezone_utils import is_weekday, get_current_hour, get_minsk_time
from services.calendar_service import is_holiday

logger = logging.getLogger(__name__)

# Глобальная переменная для хранения application бота
bot_application = None


def set_bot_application(application):
    """Установить application бота для отправки сообщений"""
    global bot_application
    bot_application = application


async def send_reminder_message(user_id):
    """
    Отправить напоминание пользователю
    """
    try:
        # Получить следующее уникальное сообщение
        message_text = get_next_unique_message(user_id)
        
        # Отправить сообщение
        if bot_application:
            await bot_application.bot.send_message(
                chat_id=user_id,
                text=message_text
            )
            
            # Пометить сообщение как отправленное
            mark_message_as_sent(user_id, message_text)
            
            logger.info(f"Сообщение отправлено пользователю {user_id}")
        else:
            logger.error("Bot application не инициализирован")
            
    except TelegramError as e:
        # Обработка ошибок Telegram (блокировка бота, недоступность и т.д.)
        if "blocked" in str(e).lower() or "chat not found" in str(e).lower():
            logger.warning(f"Пользователь {user_id} заблокировал бота или чат не найден")
        else:
            logger.error(f"Ошибка при отправке сообщения пользователю {user_id}: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при отправке сообщения: {e}")


def should_send_reminder():
    """
    Проверить, нужно ли отправлять напоминание в данный момент
    """
    # Проверка глобального состояния
    if not ScheduleSettings.is_global_enabled():
        return False
    
    # Проверка буднего дня (понедельник-четверг)
    if not is_weekday():
        return False
    
    # Проверка праздничного дня
    if is_holiday():
        return False
    
    # Проверка времени работы
    current_hour = get_current_hour()
    start_hour = ScheduleSettings.get_start_hour()
    end_hour = ScheduleSettings.get_end_hour()
    
    if not (start_hour <= current_hour < end_hour):
        return False
    
    return True


def check_and_send_reminders():
    """
    Проверить условия и отправить напоминания всем пользователям
    """
    if not should_send_reminder():
        return
    
    # Получить список пользователей с включенной напоминалкой
    enabled_users = UserSettings.get_all_enabled_users()
    
    # Если пользователей нет, использовать пользователя по умолчанию
    if not enabled_users:
        enabled_users = [USER_ID]
    
    # Отправить сообщения всем пользователям
    for user_id in enabled_users:
        # Проверка, включена ли напоминалка для пользователя
        if UserSettings.is_enabled(user_id):
            # Используем asyncio для асинхронной отправки
            import asyncio
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            loop.run_until_complete(send_reminder_message(user_id))


def start_scheduler():
    """
    Запустить планировщик в отдельном потоке
    """
    def scheduler_loop():
        """Основной цикл планировщика"""
        # Отслеживание последнего отправленного часа
        last_sent_hour = {}
        
        def check_hourly():
            """Проверить и отправить, если наступил новый час"""
            nonlocal last_sent_hour
            current_hour = get_current_hour()
            
            # Получить список пользователей
            enabled_users = UserSettings.get_all_enabled_users()
            if not enabled_users:
                enabled_users = [USER_ID]
            
            # Проверить для каждого пользователя
            for user_id in enabled_users:
                # Проверить, нужно ли отправлять в этот час
                if should_send_reminder():
                    # Проверить, не отправляли ли уже в этот час
                    user_key = str(user_id)
                    if last_sent_hour.get(user_key) != current_hour:
                        if UserSettings.is_enabled(user_id):
                            import asyncio
                            try:
                                loop = asyncio.get_event_loop()
                            except RuntimeError:
                                loop = asyncio.new_event_loop()
                                asyncio.set_event_loop(loop)
                            
                            loop.run_until_complete(send_reminder_message(user_id))
                            last_sent_hour[user_key] = current_hour
        
        # Настроить расписание: проверять каждую минуту
        schedule.every().minute.do(check_hourly)
        
        logger.info("Планировщик запущен (проверка каждый час)")
        
        while True:
            schedule.run_pending()
            time.sleep(1)  # Проверять каждую секунду для точности
    
    # Запустить планировщик в отдельном потоке
    scheduler_thread = threading.Thread(target=scheduler_loop, daemon=True)
    scheduler_thread.start()
    logger.info("Планировщик запущен в отдельном потоке")

