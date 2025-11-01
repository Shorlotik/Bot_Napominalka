"""Конфигурация бота-напоминалки"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Токен бота (из переменной окружения или по умолчанию)
BOT_TOKEN = os.getenv('BOT_TOKEN', '8100359603:AAGN64ELoSMQFQs41lPrGOE3e86LZAmHXGU')

# ID пользователя, которому отправляются сообщения
USER_ID = int(os.getenv('USER_ID', '491770320'))

# ID администратора бота
ADMIN_ID = int(os.getenv('ADMIN_ID', '791152212'))

# Настройки расписания по умолчанию
DEFAULT_START_HOUR = int(os.getenv('START_HOUR', '10'))
DEFAULT_END_HOUR = int(os.getenv('END_HOUR', '18'))

# Название файла базы данных
# Если указан путь с директорией, используется как есть, иначе создается в корне
DATABASE_NAME = os.getenv('DATABASE_NAME', 'reminder_bot.db')
# Если путь не абсолютный и не содержит директорию, создаем в data/
if DATABASE_NAME == 'reminder_bot.db' and not os.path.isabs(DATABASE_NAME):
    # Проверяем, существует ли директория data
    if not os.path.exists('data'):
        os.makedirs('data', exist_ok=True)
    DATABASE_NAME = os.path.join('data', DATABASE_NAME)

# Часовой пояс Минска
TIMEZONE = 'Europe/Minsk'

