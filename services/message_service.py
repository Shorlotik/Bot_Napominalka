"""Сервис для управления сообщениями"""
import random
from models import Message, SentMessage
from utils.message_generator import generate_message


def get_next_unique_message(user_id):
    """
    Получить следующее уникальное сообщение для пользователя.
    Если все сообщения использованы, генерирует новое.
    """
    # Получить все сообщения
    all_messages = Message.get_all()
    
    if not all_messages:
        # Если нет сообщений, создать первое
        message_id = Message.add("любимая держи спинку прямо я тебя люблю")
        message = Message.get_by_id(message_id)
        return message[1]  # Возвращаем текст сообщения
    
    # Получить список уже отправленных сообщений пользователю
    sent_message_ids = set(SentMessage.get_sent_message_ids(user_id))
    
    # Найти сообщения, которые еще не были отправлены
    available_messages = [
        msg for msg in all_messages
        if msg[0] not in sent_message_ids  # msg[0] - это id сообщения
    ]
    
    if available_messages:
        # Есть доступные сообщения, выбираем случайное
        selected_message = random.choice(available_messages)
        return selected_message[1]  # Возвращаем текст сообщения
    else:
        # Все сообщения использованы, генерируем новое
        new_message_text = generate_message()
        message_id = Message.add(new_message_text)
        return new_message_text


def mark_message_as_sent(user_id, message_text):
    """Пометить сообщение как отправленное пользователю"""
    # Найти ID сообщения по тексту
    all_messages = Message.get_all()
    message_id = None
    
    for msg in all_messages:
        if msg[1] == message_text:  # msg[1] - это текст
            message_id = msg[0]  # msg[0] - это id
            break
    
    if message_id:
        SentMessage.add(user_id, message_id)

