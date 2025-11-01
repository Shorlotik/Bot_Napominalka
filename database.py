"""Модуль для работы с базой данных SQLite"""
import sqlite3
from config import DATABASE_NAME


def get_connection():
    """Получить соединение с базой данных"""
    return sqlite3.connect(DATABASE_NAME)


def init_database():
    """Инициализация базы данных и создание таблиц"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Таблица для хранения списка сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Таблица для отслеживания отправленных сообщений
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sent_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            message_id INTEGER NOT NULL,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (message_id) REFERENCES messages(id)
        )
    ''')
    
    # Таблица для хранения состояния напоминалки пользователей
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_settings (
            user_id INTEGER PRIMARY KEY,
            is_enabled INTEGER DEFAULT 1
        )
    ''')
    
    # Таблица для хранения настроек расписания
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            start_hour INTEGER DEFAULT 10,
            end_hour INTEGER DEFAULT 18,
            is_global_enabled INTEGER DEFAULT 1,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    
    # Добавить начальное сообщение, если таблица пустая
    cursor.execute('SELECT COUNT(*) FROM messages')
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            'INSERT INTO messages (text) VALUES (?)',
            ('любимая держи спинку прямо я тебя люблю',)
        )
        conn.commit()
    
    # Добавить настройки расписания по умолчанию, если их нет
    cursor.execute('SELECT COUNT(*) FROM schedule_settings')
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            'INSERT INTO schedule_settings (start_hour, end_hour, is_global_enabled) VALUES (?, ?, ?)',
            (10, 18, 1)
        )
        conn.commit()
    
    conn.close()


if __name__ == '__main__':
    init_database()
    print("База данных инициализирована успешно!")

