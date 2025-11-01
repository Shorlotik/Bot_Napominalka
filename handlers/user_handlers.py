"""Обработчики команд для обычных пользователей"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from models import UserSettings


def get_reminder_keyboard():
    """Создать клавиатуру с кнопками управления напоминалкой"""
    keyboard = [
        [
            InlineKeyboardButton("✅ Включить напоминалку", callback_data="enable_reminder"),
            InlineKeyboardButton("❌ Выключить напоминалку", callback_data="disable_reminder")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start с клавиатурой"""
    from config import USER_ID, ADMIN_ID
    user_id = update.effective_user.id
    
    # Проверка прав доступа (разрешено пользователю и админу)
    if user_id != USER_ID and user_id != ADMIN_ID:
        await update.message.reply_text("Извините, у вас нет доступа к этому боту.")
        return
    
    # Проверка текущего состояния
    is_enabled = UserSettings.is_enabled(user_id)
    status_text = "включена" if is_enabled else "выключена"
    
    welcome_text = (
        f"Привет! Я бот-напоминалка.\n\n"
        f"Я буду напоминать тебе держать спину прямо "
        f"каждый час в будние дни с 10:00 до 18:00 по времени Минска.\n\n"
        f"Текущий статус: напоминалка {status_text}\n\n"
        f"Используй кнопки ниже для управления:"
    )
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_reminder_keyboard()
    )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик нажатий на кнопки"""
    query = update.callback_query
    await query.answer()
    
    from config import USER_ID, ADMIN_ID
    user_id = query.from_user.id
    
    # Проверка прав доступа (разрешено пользователю и админу)
    if user_id != USER_ID and user_id != ADMIN_ID:
        await query.edit_message_text("Извините, у вас нет доступа к этому боту.")
        return
    
    if query.data == "enable_reminder":
        UserSettings.set_enabled(user_id, True)
        await query.edit_message_text(
            "✅ Напоминалка включена",
            reply_markup=get_reminder_keyboard()
        )
    
    elif query.data == "disable_reminder":
        UserSettings.set_enabled(user_id, False)
        await query.edit_message_text(
            "❌ Напоминалка выключена",
            reply_markup=get_reminder_keyboard()
        )

