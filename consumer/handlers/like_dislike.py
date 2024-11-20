from sqlalchemy import update
import logging.config
from consumer.storage.db import async_session
from src.model.model import Recipe
from consumer.logger import LOGGING_CONFIG, logger


async def like_dislike(body):
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info('Прием запроса', body)
    recipe_id = body['recipe_id']
    async with async_session() as db:
        if body['action'] == 'like':
            stmt = update(Recipe).where(Recipe.id == recipe_id).values(likes=Recipe.likes + 1)
        else:
            stmt = update(Recipe).where(Recipe.id == recipe_id).values(dislikes=Recipe.dislikes + 1)
        await db.execute(stmt)
        await db.commit()
        logger.info(f'Добавление лайка/дизлайка {stmt}')
