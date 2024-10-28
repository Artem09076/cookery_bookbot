from aio_pika import Connection
from aio_pika.abc import AbstractRobustConnection
import aio_pika
from aio_pika.pool import Pool

from config.settings import settings


async def get_connection() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbit_url)

connection_pool: Pool = Pool(get_connection, max_size=10)

async def get_channel():
    async with connection_pool.acquire() as connection: #type: Connection
        return await connection.channel()

channel_pool: Pool = Pool(get_channel, max_size=10)