"""Модели данных для работы с базой данных"""
from database import get_connection


class Message:
    """Модель сообщения"""
    
    @staticmethod
    def add(text):
        """Добавить новое сообщение"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (text) VALUES (?)', (text,))
            conn.commit()
            # Принудительная синхронизация изменений
            conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
            message_id = cursor.lastrowid
            return message_id
        finally:
            conn.close()
    
    @staticmethod
    def get_all():
        """Получить все сообщения"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, text, created_at FROM messages ORDER BY id')
        messages = cursor.fetchall()
        conn.close()
        return messages
    
    @staticmethod
    def get_by_id(message_id):
        """Получить сообщение по ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, text, created_at FROM messages WHERE id = ?', (message_id,))
        message = cursor.fetchone()
        conn.close()
        return message
    
    @staticmethod
    def delete(message_id):
        """Удалить сообщение"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM messages WHERE id = ?', (message_id,))
            conn.commit()
            # Принудительная синхронизация изменений
            conn.execute('PRAGMA wal_checkpoint(TRUNCATE)')
            deleted = cursor.rowcount > 0
            return deleted
        finally:
            conn.close()
    
    @staticmethod
    def count():
        """Получить количество сообщений"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM messages')
        count = cursor.fetchone()[0]
        conn.close()
        return count


class SentMessage:
    """Модель отправленного сообщения"""
    
    @staticmethod
    def add(user_id, message_id):
        """Добавить запись об отправленном сообщении"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO sent_messages (user_id, message_id) VALUES (?, ?)',
            (user_id, message_id)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_sent_message_ids(user_id):
        """Получить список ID сообщений, отправленных пользователю"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT message_id FROM sent_messages WHERE user_id = ?',
            (user_id,)
        )
        sent_ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        return sent_ids
    
    @staticmethod
    def count_by_user(user_id):
        """Получить количество отправленных сообщений пользователю"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM sent_messages WHERE user_id = ?',
            (user_id,)
        )
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    @staticmethod
    def get_total_count():
        """Получить общее количество отправленных сообщений"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM sent_messages')
        count = cursor.fetchone()[0]
        conn.close()
        return count


class UserSettings:
    """Модель настроек пользователя"""
    
    @staticmethod
    def get(user_id):
        """Получить настройки пользователя"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT user_id, is_enabled FROM user_settings WHERE user_id = ?',
            (user_id,)
        )
        settings = cursor.fetchone()
        conn.close()
        return settings
    
    @staticmethod
    def set_enabled(user_id, is_enabled):
        """Установить состояние напоминалки для пользователя"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT OR REPLACE INTO user_settings (user_id, is_enabled) 
               VALUES (?, ?)''',
            (user_id, 1 if is_enabled else 0)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def is_enabled(user_id):
        """Проверить, включена ли напоминалка для пользователя"""
        settings = UserSettings.get(user_id)
        if settings is None:
            # По умолчанию включено
            return True
        return bool(settings[1])
    
    @staticmethod
    def get_all_enabled_users():
        """Получить список всех пользователей с включенной напоминалкой"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT user_id FROM user_settings WHERE is_enabled = 1'
        )
        users = [row[0] for row in cursor.fetchall()]
        conn.close()
        return users


class ScheduleSettings:
    """Модель настроек расписания"""
    
    @staticmethod
    def get_current():
        """Получить текущие настройки расписания"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''SELECT id, start_hour, end_hour, is_global_enabled 
               FROM schedule_settings 
               ORDER BY updated_at DESC LIMIT 1'''
        )
        settings = cursor.fetchone()
        conn.close()
        return settings
    
    @staticmethod
    def set(start_hour, end_hour, is_global_enabled):
        """Установить настройки расписания"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            '''INSERT INTO schedule_settings (start_hour, end_hour, is_global_enabled) 
               VALUES (?, ?, ?)''',
            (start_hour, end_hour, 1 if is_global_enabled else 0)
        )
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_start_hour():
        """Получить начальный час работы"""
        settings = ScheduleSettings.get_current()
        if settings:
            return settings[1]
        return 10  # По умолчанию
    
    @staticmethod
    def get_end_hour():
        """Получить конечный час работы"""
        settings = ScheduleSettings.get_current()
        if settings:
            return settings[2]
        return 18  # По умолчанию
    
    @staticmethod
    def is_global_enabled():
        """Проверить, включена ли глобально напоминалка"""
        settings = ScheduleSettings.get_current()
        if settings:
            return bool(settings[3])
        return True  # По умолчанию включено
    
    @staticmethod
    def set_global_enabled(is_enabled):
        """Установить глобальное состояние напоминалки"""
        current = ScheduleSettings.get_current()
        if current:
            start_hour = current[1]
            end_hour = current[2]
        else:
            start_hour = 10
            end_hour = 18
        ScheduleSettings.set(start_hour, end_hour, is_enabled)

