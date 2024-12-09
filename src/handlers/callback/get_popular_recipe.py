import asyncio

import aio_pika
import msgpack
from aio_pika import ExchangeType
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config.settings import settings
from src.handlers.callback.router import router
from src.handlers.state.auth import AuthGroup
from src.metrics import track_latency
from src.storage.rabbit import channel_pool
from src.templates.env import render


@router.callback_query(F.data == 'get_popular_recipe', AuthGroup.authorized)
@track_latency('get_popular_recipe')
async def get_popular_recipe(call: CallbackQuery):
    await call.message.answer('Подбираю самый популярный рецепт...')

    async with channel_pool.acquire() as channel:
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        body = {'user_id': call.from_user.id, 'action': 'get_popular_recipe'}
        await exchange.publish(aio_pika.Message(msgpack.packb(body)), routing_key='user_messages')

        user_queue_name = settings.USER_QUEUE.format(user_id=call.from_user.id)
        user_queue = await channel.declare_queue(user_queue_name, durable=True)

        retries = 3
        for _ in range(retries):
            try:
                res = await user_queue.get(timeout=3)
                await res.ack()
                data = msgpack.unpackb(res.body)
                popular_recipes = data.get('popular_recipes', [])

                for recipe in popular_recipes:
                    recipe_text = render('recipe.jinja2', recipe=recipe)

                    like_btn = InlineKeyboardButton(text='👍', callback_data=f'like_{recipe["id"]}')
                    dislike_btn = InlineKeyboardButton(text='👎', callback_data=f'dislike_{recipe["id"]}')
                    markup = InlineKeyboardMarkup(inline_keyboard=[[like_btn, dislike_btn]])

                    await call.message.answer(recipe_text, reply_markup=markup)
                return

            except asyncio.QueueEmpty:
                await asyncio.sleep(1)
        await call.message.answer('Ошибка при получении популярных рецептов. Попробуйте позже.')
