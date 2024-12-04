import aio_pika
import msgpack
from aio_pika import ExchangeType
from aiogram.types import CallbackQuery
from src.handlers.callback.router import router
from aiogram import F

from src.metrics import SEND_MESSAGE, LATENCY, track_latency
from src.storage.rabbit import channel_pool


@router.callback_query(F.data.startswith('like_') | F.data.startswith('dislike_'))
@track_latency('handle_like_dislike')
async def handle_like(call: CallbackQuery):
    action, recipe_id = call.data.split("_")
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        user_queue = await channel.declare_queue(
            'user_messages',
            durable=True
        )

        await user_queue.bind(exchange, 'user_messages')

        body = {
            'user_id': call.from_user.id,
            'recipe_id': recipe_id,
            'action': action
        }

        await exchange.publish(
            aio_pika.Message(msgpack.packb(body)),
            'user_messages'
        )
        await exchange.publish(aio_pika.Message(msgpack.packb(body)), 'user_messages')
        SEND_MESSAGE.inc()

        await call.message.delete_reply_markup()
