import uuid

import pytest
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User

from src.handlers.callback.find import find
from src.templates.env import render
from tests.mocking.tg import MockTgCall, MockTgMessage


@pytest.mark.parametrize(
    ('predefined_queue', 'correlation_id'),
    [
        (
            {
                'recipes': [
                    {'id': 1, 'recipe_title': 'Recipe 1'},
                    {'id': 2, 'recipe_title': 'Recipe 2'},
                ]
            },
            str(uuid.uuid4()),
        ),
    ],
)
@pytest.mark.usefixtures('_load_queue')
@pytest.mark.asyncio
async def test_find(predefined_queue, correlation_id) -> None:
    user = User(id=1, is_bot=False, is_premium=False, last_name='asdfdwq', first_name='asd')
    message = MockTgMessage(from_user=user)
    call = MockTgCall(from_user=user, message=message, data='see_receipts')

    await find(call=call)
    buttons = [
        [InlineKeyboardButton(text=recipe['recipe_title'], callback_data=f'info_receipts_{recipe["id"]}')]
        for recipe in predefined_queue['recipes']
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    call.message.assert_has_calls(
        [
            (
                'answer',
                (),
                {
                    'text': render('find.jinja2', res=predefined_queue['recipes']),
                    'reply_markup': keyboard,
                    'parse_mode': 'HTML'
                 }
            )
        ]
    )
