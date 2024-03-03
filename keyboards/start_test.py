from aiogram.types import KeyboardButton
from utils.questions import questions
from aiogram.utils.keyboard import ReplyKeyboardMarkup

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да')], [KeyboardButton(text='Нет')]
], resize_keyboard=True, input_field_placeholder='Готовы пройти тест?', one_time_keyboard=True)
