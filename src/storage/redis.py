from redis.asyncio import Redis, ConnectionPool

from config.settings import settings
from src.logger import logger

redis: Redis

def setup_redis():
    logger.info('Настройка подключения к Redis')
    global redis
    connection = ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    redis_ = Redis(connection_pool=connection)
    redis = redis_
    logger.info('Подключение к Redis установлено')
    return redis

def get_redis() -> Redis:
    logger.debug('Получение экземпляра Redis')
    global redis
    return redis