from aiogram.filters import Command
from aiogram.types import Message

from src.handlers.command.router import router
from src.logger import set_correlation_id, logger


@router.message(Command('start'))
async def start(message: Message):
    correlation_id = set_correlation_id()
    logger.info(f"Команда /start получена от пользователя: {message.from_user.id}, Correlation ID: {correlation_id}")
    try:
        await message.answer('Hello')
        logger.info(f"Сообщение отправлено пользователю {message.from_user.id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке сообщения пользователю {message.from_user.id}: {e}")