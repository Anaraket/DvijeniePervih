import asyncio
import os

import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from handlers.after_test import router as router_after_test
from handlers.test import router as router_test
from utils.commands import set_commands

load_dotenv()

token = os.getenv('BOT_TOKEN')
admin_id = os.getenv('ADMIN_ID')

bot = Bot(token=token, parse_mode='HTML')
dp = Dispatcher()


logging.basicConfig(level=logging.INFO)


@dp.startup()
async def start_bot():
    await bot.send_message(chat_id=admin_id, text='Бот запущен!')


async def main():
    dp.include_routers(router_test, router_after_test)
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
