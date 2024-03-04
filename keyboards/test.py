from aiogram.types import KeyboardButton
from utils.questions import questions
from aiogram.utils.keyboard import ReplyKeyboardBuilder


# Генератор клавиатуры для 1-10 вопросов
async def question(number):
    builder = ReplyKeyboardBuilder()
    for i in questions[number - 1]['answers']:
        builder.add(KeyboardButton(text=i))
    return builder.adjust(2).as_markup(resize_keyboard=True)
