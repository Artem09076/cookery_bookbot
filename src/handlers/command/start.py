from aiogram.filters import Command
from aiogram.types import Message
from aiogram.exceptions import TelegramAPIError, DetailedAiogramError, TelegramNetworkError, TelegramUnauthorizedError, TelegramServerError
import asyncio


from src.handlers.command.router import router
from src.logger import set_correlation_id, logger


@router.message(Command('start'))
async def start(message: Message):
    correlation_id = set_correlation_id()
    logger.info(f'Команда /start получена от пользователя: {message.from_user.id}, Correlation ID: {correlation_id}')
    try:
        await message.answer('Hello')
        logger.info(f'Сообщение отправлено пользователю {message.from_user.id}')
    except TelegramUnauthorizedError as e:
        logger.error(f'Ошибка при отправке сообщения, токен бота недействителен {e.message}. Пользователь {message.from_user.id}. Correlation ID: {correlation_id}')

    except TelegramNetworkError as e:
        logger.error(f'Ошибка сети {e.message} при отправке сообщения пользователю {message.from_user.id}. Correlation ID: {correlation_id}')

    except asyncio.TimeoutError:
        logger.error(f'Время ожидания истекло при отправке сообщения пользователю {message.from_user.id}. Correlation ID: {correlation_id}')
    
    except TelegramServerError as e:
        logger.error(f'Ошибка сервера Telegram {e.message} при отправке сообщения. Пользователь {message.from_user.id}. Correlation ID: {correlation_id}')

    except TelegramAPIError as e:
        logger.error(f'Ошибка API Telegram {e.message} при отправке сообщения пользователю {message.from_user.id}. Correlation ID: {correlation_id}')
    
    except DetailedAiogramError as e:
        logger.error(f'Неизвестная ошибка {e.message} при отправке сообщения пользователю {message.from_user.id}. Correlation ID: {correlation_id}')
