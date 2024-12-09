import asyncio

import aio_pika
import msgpack
from aio_pika import ExchangeType
from aio_pika.exceptions import QueueEmpty
from aiogram import F
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from config.settings import settings
from src.handlers.callback.router import router
from src.handlers.state.auth import AuthGroup
from src.metrics import SEND_MESSAGE, track_latency
from src.storage import rabbit
from src.templates.env import render


@router.callback_query(F.data == 'see_receipts', AuthGroup.authorized)
@track_latency('find_user_recipes')
async def find(call: CallbackQuery):

    async with rabbit.channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)
        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=call.from_user.id), durable=True)

        body = {'user_id': call.from_user.id, 'action': 'find'}

        await exchange.publish(aio_pika.Message(msgpack.packb(body)), 'user_messages')
        SEND_MESSAGE.inc()

        retries = 3
        for _ in range(retries):
            try:
                res = await queue.get()
                await res.ack()
                recipes = msgpack.unpackb(res.body)
                buttons = [
                    [InlineKeyboardButton(text=recipe['recipe_title'], callback_data=f'info_receipts_{recipe["id"]}')]
                    for recipe in recipes['recipes']
                ]
                keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
                await call.message.answer(
                    text=render('find.jinja2', res=recipes['recipes']), reply_markup=keyboard, parse_mode='HTML'
                )
                return
            except QueueEmpty:
                await asyncio.sleep(1)
