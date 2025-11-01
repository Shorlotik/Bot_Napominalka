"""Обработчики команд для администратора"""
from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID
from models import Message, SentMessage, UserSettings, ScheduleSettings


def is_admin(user_id):
    """Проверить, является ли пользователь администратором"""
    return user_id == ADMIN_ID


async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /admin - показать меню админ-команд"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    help_text = (
        "📋 Меню администратора:\n\n"
        "Команды для управления сообщениями:\n"
        "/add_message <текст> - Добавить новое сообщение\n"
        "/list_messages - Показать список всех сообщений\n"
        "/delete_message <id> - Удалить сообщение по ID\n\n"
        "Команды для управления напоминалкой:\n"
        "/start_reminder - Запустить напоминалку глобально\n"
        "/stop_reminder - Остановить напоминалку глобально\n"
        "/set_schedule <start_hour> <end_hour> - Изменить расписание\n\n"
        "Статистика:\n"
        "/stats - Показать статистику работы бота\n\n"
        "Справка:\n"
        "/help - Показать это меню"
    )
    
    await update.message.reply_text(help_text)


async def add_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /add_message"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "Использование: /add_message <текст сообщения>"
        )
        return
    
    message_text = " ".join(context.args)
    message_id = Message.add(message_text)
    
    await update.message.reply_text(
        f"✅ Сообщение добавлено с ID: {message_id}\n"
        f"Текст: {message_text}"
    )


async def list_messages_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /list_messages"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    messages = Message.get_all()
    
    if not messages:
        await update.message.reply_text("Список сообщений пуст.")
        return
    
    message_list = "📝 Список сообщений:\n\n"
    for msg in messages:
        message_list += f"ID: {msg[0]}\nТекст: {msg[1]}\n\n"
    
    # Telegram ограничивает длину сообщения, разбиваем если нужно
    if len(message_list) > 4096:
        # Отправить первую часть
        await update.message.reply_text(message_list[:4090] + "...")
        # TODO: Реализовать пагинацию для больших списков
    else:
        await update.message.reply_text(message_list)


async def delete_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /delete_message"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "Использование: /delete_message <id сообщения>"
        )
        return
    
    try:
        message_id = int(context.args[0])
    except ValueError:
        await update.message.reply_text("ID сообщения должен быть числом.")
        return
    
    if Message.delete(message_id):
        await update.message.reply_text(f"✅ Сообщение с ID {message_id} удалено.")
    else:
        await update.message.reply_text(
            f"❌ Сообщение с ID {message_id} не найдено."
        )


async def start_reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start_reminder"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    ScheduleSettings.set_global_enabled(True)
    await update.message.reply_text("✅ Напоминалка запущена глобально.")


async def stop_reminder_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stop_reminder"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    ScheduleSettings.set_global_enabled(False)
    await update.message.reply_text("❌ Напоминалка остановлена глобально.")


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /stats"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    total_messages = Message.count()
    total_sent = SentMessage.get_total_count()
    enabled_users = len(UserSettings.get_all_enabled_users())
    schedule_enabled = ScheduleSettings.is_global_enabled()
    start_hour = ScheduleSettings.get_start_hour()
    end_hour = ScheduleSettings.get_end_hour()
    
    stats_text = (
        "📊 Статистика работы бота:\n\n"
        f"Всего сообщений в базе: {total_messages}\n"
        f"Всего отправлено сообщений: {total_sent}\n"
        f"Пользователей с включенной напоминалкой: {enabled_users}\n"
        f"Глобальное состояние: {'Включена' if schedule_enabled else 'Выключена'}\n"
        f"Расписание: {start_hour:02d}:00 - {end_hour:02d}:00"
    )
    
    await update.message.reply_text(stats_text)


async def set_schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /set_schedule"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("У вас нет прав администратора.")
        return
    
    if len(context.args) != 2:
        await update.message.reply_text(
            "Использование: /set_schedule <start_hour> <end_hour>\n"
            "Пример: /set_schedule 10 18"
        )
        return
    
    try:
        start_hour = int(context.args[0])
        end_hour = int(context.args[1])
    except ValueError:
        await update.message.reply_text("Часы должны быть числами от 0 до 23.")
        return
    
    # Валидация
    if not (0 <= start_hour < 24) or not (0 <= end_hour < 24):
        await update.message.reply_text("Часы должны быть в диапазоне от 0 до 23.")
        return
    
    if start_hour >= end_hour:
        await update.message.reply_text(
            "Начальный час должен быть меньше конечного."
        )
        return
    
    current_enabled = ScheduleSettings.is_global_enabled()
    ScheduleSettings.set(start_hour, end_hour, current_enabled)
    
    await update.message.reply_text(
        f"✅ Расписание изменено:\n"
        f"Начало: {start_hour:02d}:00\n"
        f"Конец: {end_hour:02d}:00"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help для админа"""
    await admin_command(update, context)

