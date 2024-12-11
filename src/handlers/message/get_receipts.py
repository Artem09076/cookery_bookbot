import asyncio

import aio_pika
import msgpack
from aio_pika import ExchangeType
from aio_pika.exceptions import QueueEmpty
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from config.settings import settings
from src.handlers.message.router import router
from src.handlers.state.recipe import RecipeForm
from src.metrics import SEND_MESSAGE, track_latency
from src.storage.rabbit import channel_pool
from src.templates.env import render


def create_recipe_markup(recipe_id: int, current_page: int, total_pages: int) -> InlineKeyboardMarkup:
    like_btn = InlineKeyboardButton(text='👍', callback_data=f'like_{recipe_id}')
    dislike_btn = InlineKeyboardButton(text='👎', callback_data=f'dislike_{recipe_id}')

    pagination_buttons = []
    if current_page > 1:
        pagination_buttons.append(InlineKeyboardButton(text='⬅️ Назад', callback_data=f'page_{current_page - 1}'))
    if current_page < total_pages:
        pagination_buttons.append(InlineKeyboardButton(text='➡️ Далее', callback_data=f'page_{current_page + 1}'))

    keyboard = [[like_btn, dislike_btn], pagination_buttons]
    return InlineKeyboardMarkup(inline_keyboard=[row for row in keyboard if row])


async def show_recipe(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    recipes = data.get('recipes', [])
    current_page = data.get('current_page', 1)
    total_pages = len(recipes)

    if not recipes:
        await message.answer('Больше рецептов нет.')
        await state.clear()
        return

    current_recipe = recipes[current_page - 1]
    markup = create_recipe_markup(current_recipe['id'], current_page, total_pages)
    await message.answer(render('recipe.jinja2', recipe=current_recipe), reply_markup=markup)


@router.message(F.text.lower() == 'подобрать рецепт', RecipeForm.ingredients_collected)
@track_latency('get_receipts')
async def get_receipts(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        await message.answer("Не удалось получить данные пользователя.")
        return

    data = await state.get_data()

    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=message.from_user.id), durable=True)

        user_queue = await channel.declare_queue('user_messages', durable=True)

        await user_queue.bind(exchange, 'user_messages')
        print(data.get('ingredients'))
        body = {'user_id': message.from_user.id, 'ingredients': data.get('ingredients', []), 'action': 'get_receipts'}

        await exchange.publish(aio_pika.Message(msgpack.packb(body)), 'user_messages')

        SEND_MESSAGE.inc()

        retries = 3
        for _ in range(retries):
            try:
                res = await queue.get()
                await res.ack()
                recipes = msgpack.unpackb(res.body)['recipes']

                if not recipes:
                    await message.answer('К сожалению, рецепты не найдены по указанным ингредиентам.')
                    await state.clear()
                    return

                await state.clear()
                await state.update_data(recipes=recipes, current_page=1)
                await show_recipe(message, state)
                return
            except QueueEmpty:
                await asyncio.sleep(1)


@router.callback_query(F.data.startswith('page_'))
@track_latency('handle_pagination')
async def handle_pagination(callback_query: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    recipes = data.get('recipes', [])
    total_pages = len(recipes)

    if callback_query.data and isinstance(callback_query.data, str):
        new_page = int(callback_query.data.split('_')[1])
    else:
        await callback_query.answer('Ошибка: некорректные данные.')
        return

    if new_page < 1 or new_page > total_pages:
        await callback_query.answer('Некорректная страница.')
        return

    await state.update_data(current_page=new_page)

    if callback_query.message and isinstance(callback_query.message, Message):
        await show_recipe(callback_query.message, state)
    else:
        await callback_query.answer('Ошибка: сообщение недоступно.')

    await callback_query.answer()
