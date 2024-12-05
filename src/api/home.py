from aiogram.types import Update
from starlette.requests import Request

from src.api.router import router
from src.bot import bot, dp
from src.logger import logger, set_correlation_id


@router.post('/home')
async def home(request: Request) -> None:
    correlation_id = set_correlation_id()
    logger.info(f'Получен запрос от Telegram, Correlation ID: {correlation_id}')
    data = await request.json()
    update = Update(**data)

    await dp.feed_webhook_update(bot, update)
    logger.info(f'Обновление успешно обработано, Correlation ID: {correlation_id}')
