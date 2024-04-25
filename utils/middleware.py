import os
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message


class ChannelSubscriptionMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        if event.text:
            user_channel_status = await event.bot.get_chat_member(chat_id=os.getenv('ID_CHANNEL'),
                                                                  user_id=event.from_user.id)
            if user_channel_status.status not in ['member', 'creator', 'administrator']:
                await event.answer("Для начала подпишитесь на наш канал ☺️:")
                await event.answer(os.getenv('LINK'))
                return
        return await handler(event, data)
