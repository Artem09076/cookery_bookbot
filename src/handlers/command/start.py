from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.handlers.command.router import router
from src.handlers.state.auth import AuthGroup
from src.metrics import LATENCY, track_latency
from src.templates.env import render


@router.message(Command('start'))
@track_latency('start')
async def start(message: Message, state: FSMContext):
    await state.set_state(AuthGroup.no_authorized)
    await message.answer(render('start.jinja2'))
