import re

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, KeyboardButton, ReplyKeyboardMarkup

from src.handlers.callback.create_recipe import INGREDIENTS_REGEX
from src.handlers.callback.router import router
from aiogram import F

from src.handlers.state.recipe import RecipeForm


@router.callback_query(F.data == 'get_receipts')
async def get_receipts(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Пожалуйста напишите через запятую имеющиеся продукты')

    await state.set_state(RecipeForm.waiting_for_ingredients)


@router.message(F.text, RecipeForm.waiting_for_ingredients)
async def create_recipe(message: Message, state: FSMContext):
    if not re.match(INGREDIENTS_REGEX, message.text):
        await message.answer('Пожалуйста, введите список ингредиентов в формате: продукт1, продукт2, ...')
        return
    await state.update_data(ingredients=message.text.split(', '))
    kb_btn = KeyboardButton(text='Подобрать рецепт')
    kb = ReplyKeyboardMarkup(keyboard=[[kb_btn]], resize_keyboard=True)
    await message.answer("Продукты сохранены. Нажмите 'Подобрать рецепт', когда закончите",  reply_markup=kb)
    await state.set_state(RecipeForm.ingredients_collected)
