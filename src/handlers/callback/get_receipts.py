import re

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, KeyboardButton, Message, ReplyKeyboardMarkup

from src.handlers.callback.create_recipe import INGREDIENTS_REGEX
from src.handlers.callback.router import router
from src.handlers.state.recipe import RecipeForm
from src.metrics import LATENCY, track_latency


@router.callback_query(F.data == 'get_receipts')
@track_latency('get_user_recipe')
async def get_receipts(call: CallbackQuery, state: FSMContext):
    print("[DEBUG] get_receipts called")
    await call.message.answer('Пожалуйста напишите через запятую имеющиеся продукты')
    await state.set_state(RecipeForm.waiting_for_ingredients)


@router.message(F.text, RecipeForm.waiting_for_ingredients)
@track_latency('get_user_recipe_waiting_for_ingredients')
async def create_recipe(message: Message, state: FSMContext):
    print("[DEBUG] create_recipe called")
    if not re.match(INGREDIENTS_REGEX, message.text):
        await message.answer('Пожалуйста, введите список ингредиентов в формате: продукт1, продукт2, ...')
        return
    await state.update_data(ingredients=message.text.split(', '))
    kb_btn = KeyboardButton(text='Подобрать рецепт')
    kb = ReplyKeyboardMarkup(keyboard=[[kb_btn]], resize_keyboard=True)
    await message.answer("Продукты сохранены. Нажмите 'Подобрать рецепт', когда закончите", reply_markup=kb)
    await state.set_state(RecipeForm.ingredients_collected)
