from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import IntegrityError
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
    
    except IntegrityError:
        await session.rollback()
        return ORJSONResponse({'message': 'error adding user'}, 400)
