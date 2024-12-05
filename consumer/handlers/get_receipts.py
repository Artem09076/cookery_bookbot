import logging.config

import aio_pika
import msgpack
from aio_pika import ExchangeType
from sqlalchemy import cast, select
from sqlalchemy.dialects.postgresql import JSONB

from config.settings import settings
from consumer.logger import LOGGING_CONFIG, logger
from consumer.storage.rabbit import channel_pool
from src.model.model import Recipe
from src.storage.db import async_session


async def get_receipts(body):
    ingredients = list(set(body.get('ingredients')))

    async with async_session() as db:
        stmt = select(Recipe).where(cast(Recipe.ingredients, JSONB).op('@>')(ingredients)).order_by(Recipe.likes.desc())
        res = await db.execute(stmt)
        recipes = res.scalars().all()
        response_body = {'recipes': [recipe.to_dict() for recipe in recipes]}

    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        user_id = body.get('user_id')

        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        await queue.bind(
            exchange,
            settings.USER_QUEUE.format(user_id=user_id),
        )

        await exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)),
            routing_key=settings.USER_QUEUE.format(user_id=user_id),
        )
        logger.info(f'Отправка ответа {response_body}')
