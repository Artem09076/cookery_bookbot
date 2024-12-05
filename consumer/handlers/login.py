import logging.config

from sqlalchemy.exc import IntegrityError

from consumer.logger import LOGGING_CONFIG, logger
from consumer.storage.db import async_session
from src.model.model import User


async def login(body):
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info('Прием запроса', body)
    async with async_session() as db:
        user = User(user_id=body.get('user_id'))
        db.add(user)

        try:
            await db.commit()
            logger.info(f'Пользователь {user} зарегистрировался')
        except IntegrityError:
            print('Такой пользователь уже существует')
            await db.rollback()
