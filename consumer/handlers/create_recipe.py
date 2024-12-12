import logging.config
from typing import Any, Dict

from sqlalchemy import select

from consumer.logger import LOGGING_CONFIG, logger
from src.model.model import Recipe, User
from src.storage.db import async_session


async def create_recipe(body: Dict[str, Any]) -> None:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger.info('Прием запроса', body)
    async with async_session() as db:
        user = (await db.execute(select(User).where(User.user_id == body.get('user_id')))).one()[0]
        recipe = Recipe(
            user_id=body.get('user_id'),
            recipe_title=body.get('recipe_title'),
            ingredients=body.get('ingredients'),
            description_recipe=body.get('description_recipe'),
            user=user,
        )
        db.add(recipe)
        await db.commit()
