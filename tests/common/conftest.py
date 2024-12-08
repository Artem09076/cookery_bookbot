from collections import deque
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock

import msgpack
import pytest
import pytest_asyncio
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from consumer.storage import db as consumer_db, rabbit as consumer_rabbit
from src import bot
from src.storage import db, rabbit, redis
from src.storage.db import engine, get_db
from tests.mocking.rabbit import MockChannel, MockChannelPool, MockExchange, MockQueue
from tests.mocking.redis import MockRedis


@pytest_asyncio.fixture(autouse=True)
async def db_session(app: FastAPI, monkeypatch: pytest.MonkeyPatch) -> AsyncSession:
    async with engine.begin() as conn:
        session_maker = async_sessionmaker(bind=conn, class_=AsyncSession)
        async with session_maker() as session:

            async def overrided_db_session() -> AsyncGenerator[AsyncSession, None]:
                yield session

            monkeypatch.setattr(consumer_db, 'async_session', session_maker)
            monkeypatch.setattr(db, 'async_session', session_maker)
            app.dependency_overrides[get_db] = overrided_db_session
            yield session

        await conn.rollback()


@pytest.fixture(autouse=True)
def mock_bot_dp(monkeypatch: pytest.MonkeyPatch) -> AsyncMock:
    mock = AsyncMock()

    monkeypatch.setattr(bot, 'dp', mock)
    return mock


@pytest.fixture(autouse=True)
def _mock_redis(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(redis, 'redis_storage', MockRedis())
    return


@pytest.fixture
def mock_exchange() -> MockExchange:
    return MockExchange()


@pytest_asyncio.fixture()
async def _load_queue(monkeypatch: pytest.MonkeyPatch, predefined_queue: Any, mock_exchange: MockExchange):
    queue = MockQueue(deque())

    if predefined_queue is not None:
        await queue.put(msgpack.packb(predefined_queue))

    channel = MockChannel(queue=queue, exchange=mock_exchange)

    pool = MockChannelPool(channel=channel)

    monkeypatch.setattr(rabbit, 'channel_pool', pool)
    monkeypatch.setattr(consumer_rabbit, 'channel_pool', pool)
