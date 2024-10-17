from sqlalchemy.exc import IntegrityError

from src.storage.db import engine
from src.model.meta import Base
import asyncio
from src.logger import logger


async def init_models():
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info('Инициализация базы данных прошла успешно.')
    except IntegrityError:
        logger.warning('База данных уже существует. Повторная инициализация не требуется.')
    except Exception as e:
        logger.exception(f'Ошибка при инициализации базы данных: {e}')

if __name__ == '__main__':
    asyncio.run(init_models())