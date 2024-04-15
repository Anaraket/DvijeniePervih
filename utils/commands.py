from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


# menu в чате с ботом
async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Запуск бота и прохождение тестирования'
        ),
        BotCommand(
            command='help',
            description='Помощь в работе с ботом'
        ),
        BotCommand(
            command='channel',
            description='Ссылка на канал',
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())
