import asyncio

import aio_pika
import msgpack
from aio_pika import ExchangeType
from aio_pika.exceptions import QueueEmpty
from aiogram import F
from aiogram.types import CallbackQuery, Message

from config.settings import settings
from src.handlers.callback.router import router
from src.handlers.state.auth import AuthGroup
from src.metrics import SEND_MESSAGE, track_latency
from src.storage.rabbit import channel_pool
from src.templates.env import render


@router.callback_query(F.data.startswith('info_receipts'), AuthGroup.authorized)
@track_latency('request_recipe_info')
async def request_recipe_info(call: CallbackQuery) -> None:
    if call.data:
        recipe_id = call.data.split('_')[2]
    else:
        return
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=call.from_user.id), durable=True)
        user_queue = await channel.declare_queue('user_messages', durable=True)

        await queue.bind(exchange, settings.USER_QUEUE.format(user_id=call.from_user.id))

        await user_queue.bind(exchange, 'user_messages')

        body = {'recipe_id': recipe_id, 'action': 'info_receipts', 'user_id': call.from_user.id}

        await exchange.publish(aio_pika.Message(msgpack.packb(body)), 'user_messages')

        SEND_MESSAGE.inc()

        retries = 3
        for _ in range(retries):
            try:
                result = await queue.get()
                await result.ack()
                response = msgpack.unpackb(result.body)
                recipe = response.get('recipe')
                if recipe:
                    if call.message and isinstance(call.message, Message):
                        await call.message.answer(text=render('recipe_info.jinja2', recipe=recipe), parse_mode='HTML')
                    else:
                        await call.answer('Ошибка: сообщение недоступно.')
                else:
                    if call.message and isinstance(call.message, Message):
                        await call.message.answer(text='Рецепт не найден.', parse_mode='HTML')
                    else:
                        await call.answer('Ошибка: сообщение недоступно.')
                return

            except QueueEmpty:
                await asyncio.sleep(1)
