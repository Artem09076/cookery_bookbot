from sqlalchemy.exc import IntegrityError

from src.storage.db import engine
from src.model.meta import Base
import asyncio
import logging

async def init_models():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except IntegrityError:
        logging.exception('DB already exist')

if __name__ == '__main__':
    asyncio.run(init_models())