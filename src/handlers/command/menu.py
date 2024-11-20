from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

from src.handlers.command.router import router
from src.templates.env import render


@router.message(Command('menu'))
async def menu(message: Message):
    inline_kb_list = [
        [InlineKeyboardButton(text='Создать новый рецепт', callback_data='new_receipt')],
        [InlineKeyboardButton(text='Получить рецепт по продуктам', callback_data='get_receipts')],
        [InlineKeyboardButton(text='Подобрать самый популярный рецепт', callback_data='find_receipts')],
        [InlineKeyboardButton(text='Посмотреть свои рецепты', callback_data='see_receipts')]
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_kb_list)
    await message.answer(render('menu.jinja2'), reply_markup=reply_markup)
