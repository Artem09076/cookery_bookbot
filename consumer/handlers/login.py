from sqlalchemy.exc import IntegrityError

from consumer.storage.db import async_session
from src.model.model import User


async def login(body):
    async with async_session() as db:
        user = User(user_id=body.get('user_id'))
        db.add(user)

        try:
            await db.commit()
        except IntegrityError:
            print('Такой пользователь уже существует')
            await db.rollback()