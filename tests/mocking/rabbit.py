import uuid
from collections import deque
from dataclasses import dataclass
from typing import Iterator
from unittest.mock import AsyncMock

from aio_pika.exceptions import QueueEmpty


@dataclass
class MockChannelPool:
    channel: 'MockChannel'

    def acquire(self):
        return self.channel


@dataclass
class MockChannel:
    queue: 'MockQueue'
    exchange: 'MockExchange'

    def __aenter__(self):
        return self

    def __await__(self):
        yield
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb):
        return self

    async def set_qos(self, *args, **kwargs) -> None:
        return

    async def declare_queue(self, *args, **kwargs):
        return self.queue

    async def declare_exchange(self, *args, **kwargs):
        return self.exchange


class MockQueueIterator:
    def __init__(self, queue: deque['MockMessage']):
        self.queue: Iterator['MockMessage'] = iter(queue)

    def __aiter__(self) -> 'MockQueueIterator':
        return self

    async def __anext__(self) -> 'MockMessage':
        return next(self.queue)

    def __aenter__(self) -> 'MockQueueIterator':
        return self

    def __await__(self) -> 'MockQueueIterator':
        yield
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb) -> 'MockQueueIterator':
        return self


@dataclass
class MockQueue:
    queue: deque['MockMessage']

    async def get(self, *args, **kwargs) -> 'MockMessage':
        try:
            return self.queue.popleft()
        except IndexError:
            raise QueueEmpty

    async def iterator(self) -> MockQueueIterator:
        return MockQueueIterator(queue=self.queue)

    async def put(self, value: bytes):
        self.queue.append(MockMessage(body=value))


class MockMessageProcess:
    def __aenter__(self) -> MockQueueIterator:
        return self

    def __await__(self) -> MockQueueIterator:
        yield
        return self

    def __aexit__(self, exc_type, exc_val, exc_tb) -> MockQueueIterator:
        return self


@dataclass
class MockMessage:
    body: bytes

    def process(self) -> MockMessageProcess:
        return MockMessageProcess()

    @property
    def correlation_id(self):
        return str(uuid.uuid4())


class MockExchange(AsyncMock):
    pass
