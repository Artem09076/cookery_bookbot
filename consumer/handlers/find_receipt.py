import logging.config

import aio_pika
import msgpack
from aio_pika import ExchangeType
from sqlalchemy.future import select

from config.settings import settings
from consumer.logger import LOGGING_CONFIG, logger
from consumer.storage.db import async_session
from src.model.model import Recipe
from consumer.storage import rabbit

async def find_receipt(body):
    logging.config.dictConfig(LOGGING_CONFIG)
    user_id = body.get('user_id')
    async with async_session() as db:
        result = await db.execute(select(Recipe).where(Recipe.user_id == user_id))
        recipes = result.scalars().all()
        response_body = {'recipes': [recipe.to_dict() for recipe in recipes]}
    async with rabbit.channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=user_id), durable=True)

        await exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)), routing_key=settings.USER_QUEUE.format(user_id=user_id)
        )
        logger.info('Отправка ответа', response_body)
