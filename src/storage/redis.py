from redis.asyncio import Redis, ConnectionPool

from config.settings import settings

redis: Redis

def setup_redis():
    global redis

    connection = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

    redis_ = Redis(connection_pool=connection)

    redis = redis_

    return redis

def get_redis() -> Redis:
    global redis


    return redis