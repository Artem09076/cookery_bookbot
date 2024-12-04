import aio_pika
import msgpack
from aio_pika import ExchangeType
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config.settings import settings
from src.handlers.command.router import router
from src.handlers.state.auth import AuthGroup
from src.metrics import LATENCY, SEND_MESSAGE, track_latency
from src.storage.rabbit import channel_pool


@router.message(Command('login'))
@track_latency('login')
async def login(message: Message, state: FSMContext):
    async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
        exchange = await channel.declare_exchange('user_receipts', ExchangeType.TOPIC, durable=True)
        queue = await channel.declare_queue(settings.USER_QUEUE.format(user_id=message.from_user.id), durable=True)
        user_queue = await channel.declare_queue('user_messages', durable=True)

        await queue.bind(exchange, settings.USER_QUEUE.format(user_id=message.from_user.id))

        await user_queue.bind(exchange, 'user_messages')

        body = {'user_id': message.from_user.id, 'action': 'login'}

        await exchange.publish(aio_pika.Message(msgpack.packb(body)), 'user_messages')

        SEND_MESSAGE.inc()

    await state.set_state(AuthGroup.authorized)
    await message.answer('Прекрасно, вы зарегистрированы. Для начала работы введи команду /menu ')
