import logging.config

from sqlalchemy import update

from consumer.logger import LOGGING_CONFIG, logger
from consumer.storage.db import async_session
from src.model.model import Recipe


async def like_dislike(body):
    recipe_id = body['recipe_id']
    async with async_session() as db:
        if body['action'] == 'like':
            stmt = update(Recipe).where(Recipe.id == recipe_id).values(likes=Recipe.likes + 1)
        else:
            stmt = update(Recipe).where(Recipe.id == recipe_id).values(dislikes=Recipe.dislikes + 1)
        await db.execute(stmt)
        await db.commit()
        logger.info(f'Добавление лайка/дизлайка {stmt}')
