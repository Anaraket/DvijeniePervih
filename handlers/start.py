from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command(commands=['start']))
async def command_start(message: Message, bot: Bot):
    await bot.send_message(chat_id=message.from_user.id, text="👋 Привет! Это бот для прохождения теста")
