from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

result_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Посмотреть ошибки')],
    [KeyboardButton(text='Получить сертификат')]
], resize_keyboard=True, one_time_keyboard=True)