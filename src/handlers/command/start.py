from aiogram.filters import Command
from aiogram.types import Message

from src.handlers.command.router import router


@router.message(Command('start'))
async def start(message: Message):
    await message.answer('Hello')