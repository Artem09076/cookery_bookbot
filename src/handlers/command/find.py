import msgpack
from aio_pika import ExchangeType
from aio_pika.exceptions import QueueEmpty
from aiogram.filters import Command

from aiogram.types import Message
import asyncio
import aio_pika

from config.settings import settings
from src.handlers.command.router import router
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

        retries = 3
        for _ in range(retries):
            try:
                res = await queue.get()
                await res.ack()
                recipes = msgpack.unpackb(res.body)
                await  message.answer(render('find.jinja2', res=recipes['recipes']))
                return
            except QueueEmpty:
                await asyncio.sleep(1)