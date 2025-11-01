"""Утилиты для работы с часовым поясом Минска"""
import pytz
from datetime import datetime


def get_minsk_time():
    """Получить текущее время в часовом поясе Минска"""
    minsk_tz = pytz.timezone('Europe/Minsk')
    return datetime.now(minsk_tz)


def is_weekday(date=None):
    """
    Проверить, является ли день будним (понедельник-пятница)
    Возвращает True для понедельника (0) - пятницы (4)
    """
    if date is None:
        date = get_minsk_time()
    # Понедельник = 0, Вторник = 1, Среда = 2, Четверг = 3, Пятница = 4
    return date.weekday() <= 4


def is_work_hour(hour, start_hour=10, end_hour=18):
    """
    Проверить, находится ли указанный час в диапазоне работы
    """
    return start_hour <= hour < end_hour


def get_current_hour():
    """Получить текущий час в Минске"""
    return get_minsk_time().hour


def get_current_weekday():
    """Получить текущий день недели (0=понедельник, 6=воскресенье)"""
    return get_minsk_time().weekday()

