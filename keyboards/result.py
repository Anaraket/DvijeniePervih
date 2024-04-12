from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура после завершения теста
result_kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Получить сертификат')]
], resize_keyboard=True, one_time_keyboard=False)
