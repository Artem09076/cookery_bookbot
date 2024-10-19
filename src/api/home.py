from aiogram.types import Update
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from aiogram.exceptions import TelegramAPIError, DetailedAiogramError, TelegramNetworkError, TelegramUnauthorizedError, TelegramServerError
import asyncio

from src.api.router import router
from src.bot import get_dp, get_bot
from src.storage.db import get_db
from src.logger import set_correlation_id, logger


@router.post('/home')
async def home(request: Request) -> None:
    correlation_id = set_correlation_id()
    logger.info(f'Получен запрос от Telegram, Correlation ID: {correlation_id}')
    try:
        data = await request.json()
        update = Update(**data)
        dp = get_dp()
        await dp.feed_webhook_update(get_bot(), update)
        logger.info(f'Обновление успешно обработано, Correlation ID: {correlation_id}')
    except TelegramUnauthorizedError as e:
        logger.error(f'Ошибка при обновлении, токен бота недействителен {e.message}. Correlation ID: {correlation_id}')

    except TelegramNetworkError as e:
        logger.error(f'Ошибка сети {e.message} при обновлении. Correlation ID: {correlation_id}')

    except asyncio.TimeoutError:
        logger.error(f'Время ожидания истекло при обновлении. Correlation ID: {correlation_id}')

    except TelegramServerError as e:
        logger.error(f'Ошибка сервера Telegram {e.message} при обновлении. Correlation ID: {correlation_id}')

    except TelegramAPIError as e:
        logger.error(f'Ошибка API Telegram {e.message} при обновлении. Correlation ID: {correlation_id}')

    except DetailedAiogramError as e:
        logger.error(f'Неизвестная ошибка {e.message} при обновлении. Correlation ID: {correlation_id}')
