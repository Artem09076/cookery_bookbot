import msgpack
from aio_pika import ExchangeType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError, DetailedAiogramError, TelegramNetworkError, TelegramUnauthorizedError, TelegramServerError
import asyncio
import aio_pika

from config.settings import settings
from src.handlers.command.router import router
from src.handlers.state.auth import AuthGroup
from src.logger import set_correlation_id, logger
from src.storage.rabbit import channel_pool
from src.templates.env import render


@router.message(Command('find'))
async def find(message: Message):

    async with channel_pool.acquire() as channel: # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)
        queue = await channel.declare_queue(
            settings.USER_QUEUE.format(user_id=message.from_user.id),
            durable=True
        )
        user_queue = await channel.declare_queue(
            'user_messages',
            durable=True
        )

        await queue.bind(exchange,
                         settings.USER_QUEUE.format(user_id=message.from_user.id)
                         )

        await user_queue.bind(exchange, 'user_messages')

        body = {
            'user_id': message.from_user.id,
            'action': 'find'
        }

        await exchange.publish(
            aio_pika.Message(msgpack.packb(body)),
            'user_messages'
        )


        res = await queue.get()
        recipes = msgpack.unpackb(body)
        await  message.answer(render('find.jinja2', res=recipes['recipes']))






