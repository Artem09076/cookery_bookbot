import aio_pika
import msgpack
from aio_pika import ExchangeType
from aiogram import F
from aiogram.types import CallbackQuery, Message

from src.handlers.callback.router import router
from src.metrics import SEND_MESSAGE, track_latency
from src.storage.rabbit import channel_pool


@router.callback_query(F.data.startswith('like_') | F.data.startswith('dislike_'))
@track_latency('handle_like_dislike')
async def handle_like(call: CallbackQuery) -> None:
    if call.data:
        action, recipe_id = call.data.split('_')
    else:
        return
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        user_queue = await channel.declare_queue('user_messages', durable=True)

        await user_queue.bind(exchange, 'user_messages')

        body = {'user_id': call.from_user.id, 'recipe_id': recipe_id, 'action': action}

        await exchange.publish(aio_pika.Message(msgpack.packb(body)), 'user_messages')
        SEND_MESSAGE.inc()

        if call.message and isinstance(call.message, Message):
            await call.message.delete_reply_markup()
        else:
            await call.answer('Ошибка: сообщение недоступно.')
