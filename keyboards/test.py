import os

from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from utils.db import Database


# Генератор клавиатуры для 1-10 вопросов
async def question(number, category):
    builder = ReplyKeyboardBuilder()
    db = Database(os.getenv('DATABASE_NAME'))
    answers = db.get_answers_from_db(category, number)
    for i in answers:
        builder.add(KeyboardButton(text=i))
    return builder.adjust(1).as_markup(resize_keyboard=True)
