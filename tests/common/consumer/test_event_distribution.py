import uuid

import aio_pika
import msgpack
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.settings import settings
from consumer.app import main
from src.model.model import Recipe
from tests.mocking.rabbit import MockExchange


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('predefined_queue', 'correlation_id'),
    [
        (
            {'action': 'find', 'user_id': 1},
            str(uuid.uuid4()),
        ),
    ],
)
@pytest.mark.usefixtures('_load_seeds', '_load_queue')
async def test_event_distribution(
    db_session: AsyncSession, predefined_queue, correlation_id, mock_exchange: MockExchange
):
    await main()
    expected_routing_key = settings.USER_QUEUE.format(user_id=predefined_queue['user_id'])

    async with db_session:
        not_fetched = await db_session.execute(select(Recipe).where(Recipe.user_id == predefined_queue['user_id']))
        recipes = not_fetched.scalars().all()
        expected_message = aio_pika.Message(
            msgpack.packb({'recipes': [recipe.to_dict() for recipe in recipes]}), correlation_id=correlation_id
        )

    mock_exchange.assert_has_calls(
        [
            ('publish', (expected_message,), {'routing_key': expected_routing_key}),
        ]
    )
