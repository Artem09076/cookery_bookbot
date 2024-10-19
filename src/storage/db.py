from collections.abc import AsyncGenerator

from asyncpg import Connection
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from src.logger import logger
from config.settings import settings

from src.model.meta import Base

import asyncio



def create_engine() -> AsyncEngine:
    logger.info('Создание движка для подключения к базе данных')
    return create_async_engine(settings.db_url, poolclass = AsyncAdaptedQueuePool, connect_args={'connection_class': Connection,})


def create_session(_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    logger.info('Создание сессии для взаимодействия с базой данных')
    return async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )


engine = create_engine()
async_session = create_session(engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug('Получение сессии базы данных')
    async with async_session() as db:
        yield db
    logger.debug('Закрытие сессии базы данных')