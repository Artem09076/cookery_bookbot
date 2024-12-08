import aio_pika
import msgpack
from aio_pika import ExchangeType
from sqlalchemy.future import select

from config.settings import settings
from consumer.storage.db import async_session
from src.model.model import Recipe
from src.storage.rabbit import channel_pool


async def on_message(body):
    action = body.get('action')
    if action == 'info_receipts':
        recipe_id = body.get('recipe_id')

        async with async_session() as db:
            result = await db.execute(select(Recipe).where(Recipe.id == recipe_id))
            rec = result.scalar_one_or_none()

            if rec:
                response_body = {'recipe': rec.to_dict()}
            else:
                response_body = {'recipe': None}

        async with channel_pool.acquire() as channel:
            user_id = body.get('user_id')
            exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

            queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

            await queue.bind(
                exchange,
                settings.USER_QUEUE.format(user_id=user_id),
            )

            await exchange.publish(
                aio_pika.Message(msgpack.packb(response_body)), routing_key=settings.USER_QUEUE.format(user_id=user_id)
            )
