import msgpack
from aio_pika import ExchangeType
from sqlalchemy.exc import IntegrityError

from config.settings import settings
from consumer.storage.db import async_session
from consumer.storage.rabbit import channel_pool
from src.model.model import User
import aio_pika
async def login(body):
    async with channel_pool.acquire() as channel: # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)
        async with async_session() as db:
            user = User(user_id=body['user_id'])
            db.add(user)
            try:
                await db.commit()
                res = 'Yes'
            except IntegrityError:
                print('Такой пользователь уже существует')
                await db.rollback()
                res = 'No'
        await exchange.publish(
            aio_pika.Message(
                msgpack.packb(res)
            ),
            routing_key=settings.USER_QUEUE.format(user_id=body['user_id'])
        )