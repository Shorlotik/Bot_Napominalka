"""Сервис для работы с API календаря праздничных дней"""
import logging
from datetime import datetime
from utils.timezone_utils import get_minsk_time

logger = logging.getLogger(__name__)

# Резервный список основных праздничных дней Беларуси (месяц, день)
RESERVE_HOLIDAYS = [
    (1, 1),   # 1 января - Новый год
    (1, 7),   # 7 января - Рождество
    (3, 8),   # 8 марта - Международный женский день
    (5, 1),   # 1 мая - Праздник труда
    (5, 9),   # 9 мая - День Победы
    (7, 3),   # 3 июля - День независимости
    (11, 7),  # 7 ноября - День Октябрьской революции
    (12, 25), # 25 декабря - Рождество
]

# Кэш праздничных дней для текущего года
_holidays_cache = {}


def fetch_holidays_from_api(year):
    """
    Получить праздничные дни через API
    В случае ошибки возвращает None
    """
    # TODO: Реализовать получение через Calendarific API или Holidays API
    # Пока возвращаем None, используем резервный список
    try:
        # Пример использования Calendarific API (нужен API ключ):
        # import requests
        # api_key = "YOUR_API_KEY"
        # url = f"https://calendarific.com/api/v2/holidays"
        # params = {
        #     "api_key": api_key,
        #     "country": "BY",
        #     "year": year
        # }
        # response = requests.get(url, params=params)
        # if response.status_code == 200:
        #     data = response.json()
        #     holidays = [datetime.strptime(h["date"]["iso"], "%Y-%m-%d") for h in data["response"]["holidays"]]
        #     return holidays
        return None
    except Exception as e:
        logger.error(f"Ошибка при получении праздничных дней через API: {e}")
        return None


def get_holidays_for_year(year):
    """
    Получить список праздничных дней для указанного года
    Автоматически очищает кэш для других годов
    """
    current_year = get_minsk_time().year
    
    # Очистить кэш для других годов (кроме текущего)
    if year != current_year:
        # Оставить только текущий год в кэше
        if current_year in _holidays_cache:
            temp_cache = {current_year: _holidays_cache[current_year]}
            _holidays_cache.clear()
            _holidays_cache.update(temp_cache)
    
    # Проверить кэш
    if year in _holidays_cache:
        return _holidays_cache[year]
    
    # Попытаться получить через API
    api_holidays = fetch_holidays_from_api(year)
    
    if api_holidays:
        holidays = api_holidays
    else:
        # Использовать резервный список
        holidays = []
        for month, day in RESERVE_HOLIDAYS:
            try:
                date = datetime(year, month, day)
                holidays.append(date)
            except ValueError:
                # Пропустить невалидные даты (например, 29 февраля в невисокосном году)
                pass
    
    # Сохранить в кэш
    _holidays_cache[year] = holidays
    return holidays


def is_holiday(date=None):
    """
    Проверить, является ли указанная дата праздничным днем
    Автоматически обновляет кэш при смене года
    """
    if date is None:
        date = get_minsk_time().date()
    elif isinstance(date, datetime):
        date = date.date()
    
    year = date.year
    current_year = get_minsk_time().year
    
    # Очистить кэш при смене года
    if year != current_year and year in _holidays_cache:
        # Очистить кэш для старого года (опционально, можно оставить для истории)
        pass
    
    # Получить праздники для указанного года (автоматически очистит кэш для других годов)
    holidays = get_holidays_for_year(year)
    
    # Проверить, есть ли дата в списке праздников
    for holiday in holidays:
        if isinstance(holiday, datetime):
            if holiday.date() == date:
                return True
        else:
            if holiday == date:
                return True
    
    return False


def clear_cache():
    """Очистить кэш праздничных дней"""
    global _holidays_cache
    _holidays_cache = {}

