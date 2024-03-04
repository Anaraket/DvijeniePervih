from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardMarkup

# Клавиатура на подтверждение прохождения теста
kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Да')],
    [KeyboardButton(text='Нет')]
], resize_keyboard=True, input_field_placeholder='Готовы пройти тест?', one_time_keyboard=True)
