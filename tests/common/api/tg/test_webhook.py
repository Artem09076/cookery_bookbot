from datetime import datetime
from unittest.mock import AsyncMock

import pytest
from aiogram.types import Chat, Message, Update, User


@pytest.mark.asyncio
async def test_webhook(http_client, mock_bot_dp: AsyncMock):
    chat = Chat(id=1, type='private')
    user = User(id=1, is_bot=False, is_premium=False, last_name='asdfdwq', first_name='asd')
    message = Message(message_id=1, date=datetime.now(), chat=chat, from_user=user)
    update = Update(update_id=1, message=message).model_dump(mode='json')

    request = await http_client.post('/home', json=update)
    # mock_bot_dp.assert_has_calls([
    #     call.feed_webhook_update(bot.bot, update)
    # ])

    assert request.status_code == 200
    assert request.json() == {'status': 'ok'}
