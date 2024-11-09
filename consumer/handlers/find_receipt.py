from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from consumer.storage.db import async_session
from src.model.model import Recipe, User
import aio_pika
import msgpack
from aio_pika import ExchangeType
from src.storage.rabbit import channel_pool
from config.settings import settings

async def find_receipt(body):
    user_id = body.get("user_id")
    async with async_session() as db:
        result = await db.execute(select(Recipe).where(Recipe.user_id == user_id))
        recipes = result.scalars().all()
        response_body = {
            'recipes': [
                {"recipe_title": recipe.recipe_title}
                for recipe in recipes
            ]
        }

    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(
            settings.USER_QUEUE.format(user_id=user_id),
            durable=True
        )

        await queue.bind(
            exchange,
            settings.USER_QUEUE.format(user_id=user_id),
        )

        await exchange.publish(
            aio_pika.Message(msgpack.packb(response_body)),
            routing_key=settings.USER_QUEUE.format(user_id=user_id)
        )


