from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import Command
import os
from utils.db import Database

router = Router()


@router.message(Command(commands=['start']))
async def command_start(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    await bot.send_message(chat_id=message.from_user.id, text="👋 Привет! Это бот для прохождения теста")
