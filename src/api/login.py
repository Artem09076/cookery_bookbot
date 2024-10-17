from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router import router
from src.schema.login import AuthResponse, AuthPost
from src.storage.db import get_db
from src.model.model import User
from src.logger import set_correlation_id, logger
from aiogram.exceptions import TelegramAPIError, DetailedAiogramError, TelegramNetworkError, TelegramUnauthorizedError, TelegramServerError, TelegramBadRequest
import asyncio


@router.post('/login', response_model=AuthResponse)
async def login(body: AuthPost, session: AsyncSession = Depends(get_db)):
    correlation_id = set_correlation_id()
    logger.info(f'Попытка входа пользователя с ID: {body.user_id}, Correlation ID: {correlation_id}')
    user = User(user_id=body.user_id)
    session.add(user)
    try:
        await session.commit()
        logger.info(f'Пользователь с ID: {body.user_id} успешно добавлен, Correlation ID: {correlation_id}')
        return ORJSONResponse({'message': 'user add'}, 200)
    
    except TelegramBadRequest as e:
        logger.warning(f'Неправильный запрос {e.message} от пользователя с ID: {body.user_id}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 400)

    except TelegramUnauthorizedError as e:
        logger.error(f'Ошибка при добавлении пользователя с ID: {body.user_id}, токен бота недействителен {e.message}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 401)

    except TelegramNetworkError as e:
        logger.error(f'Ошибка сети {e.message} при добавлении пользователя с ID: {body.user_id}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 503)

    except asyncio.TimeoutError:
        logger.error(f'Время ожидания истекло при добавлении пользователя с ID: {body.user_id}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 504)

    except TelegramServerError as e:
        logger.error(f'Ошибка сервера Telegram {e.message} при добавлении пользователя с ID: {body.user_id}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 500)

    except TelegramAPIError as e:
        logger.error(f'Ошибка API Telegram {e.message} при добавлении пользователя с ID: {body.user_id}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 500)

    except DetailedAiogramError as e:
        logger.error(f'Неизвестная ошибка {e.message} при добавлении пользователя с ID: {body.user_id}. Correlation ID: {correlation_id}')
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 400)
