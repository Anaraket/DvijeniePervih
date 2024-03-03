from aiogram import Bot, Dispatcher, F
import asyncio
import logging
from aiogram.types import Message
from bd import conn, cursor

from handlers.start import router

from dotenv import load_dotenv
import os
from utils.commands import set_commands

load_dotenv()

token = os.getenv('TOKEN_API')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.startup()
async def start_bot(bot: Bot):
    await bot.send_message(chat_id=admin_id, text='Бот запущен!')

# Проверка подписки на канал
@dp.message(F.text.lower().in_(['/test', 'пройти тест', 'тест']))
async def check_subscription(message: Message):
    user_channel_status = await bot.get_chat_member(chat_id=-1002004860176, user_id=message.from_user.id)
    if user_channel_status.status != 'left':
        # Занесение пользователя в базу данных
        cursor.execute('''
            INSERT OR IGNORE INTO users (telegram_id, status)
            VALUES (?, ?)
        ''', (message.from_user.id, user_channel_status.status))
        conn.commit()

        await message.answer('Желаете пройти тест? (да/нет)')
    else:
        await message.answer('Для начала подпишись на наш канал: https://t.me/+iv10xEEruWNmOWJi')


@dp.message(F.text.lower.in_(['да', 'хочу', 'конечно', 'желаю']))
async def pozitive_answer(message: Message):
    await message.answer("Введите ФИО: ")


async def main():
    dp.include_router(router=router)
    await set_commands(bot)
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('exit')
conn.close()
