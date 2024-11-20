import asyncio

import aio_pika
import msgpack
from aio_pika import ExchangeType
from aio_pika.exceptions import QueueEmpty
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from config.settings import settings
from src.handlers.message.router import router
from aiogram import F

from src.handlers.state.recipe import RecipeForm
from src.storage.rabbit import channel_pool
from src.templates.env import render


@router.message(F.text.lower() == 'подобрать рецепт', RecipeForm.ingredients_collected)
async def get_receipts(message: Message, state: FSMContext):
    data = await state.get_data()
    # await message.delete_reply_markup()

    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(
            settings.USER_QUEUE.format(user_id=message.from_user.id),
            durable=True
        )

        user_queue = await channel.declare_queue(
            'user_messages',
            durable=True
        )

        await user_queue.bind(exchange, 'user_messages')

        body = {
            'user_id': message.from_user.id,
            'ingredients': data.get('ingredients', []),
            'action': 'get_receipts'
        }

        await exchange.publish(
            aio_pika.Message(msgpack.packb(body)),
            'user_messages'
        )
        retries = 3
        for _ in range(retries):
            try:
                res = await queue.get()
                await res.ack()
                recipes = msgpack.unpackb(res.body)['recipes']

                like_btn = InlineKeyboardButton(text='👍', callback_data=f'like_{recipes[0]['id']}')
                dislike_btn = InlineKeyboardButton(text='👎', callback_data=f'dislike_{recipes[0]['id']}')
                markup = InlineKeyboardMarkup(
                    inline_keyboard=[[like_btn, dislike_btn], ]
                )

                await message.answer(render('recipe.jinja2', recipe=recipes[0]), reply_markup=markup)
                await state.clear()
                return
            except QueueEmpty:
                await asyncio.sleep(1)
