from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# menu в чате с ботом
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запускаем бота'
        ),
        BotCommand(
            command='test',
            description='Пройти тест'
        ),
        BotCommand(
            command='help',
            description='Помощь в работе с ботом'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
