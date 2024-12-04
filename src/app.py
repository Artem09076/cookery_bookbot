import asyncio
from contextlib import contextmanager, asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI

from config.settings import settings
from src.api.router import router
from src.bot import dp, bot
from src.handlers.callback.router import router as callback_router
from src.handlers.command.router import router as command_router
from src.handlers.message.router import router as message_router
from src.log_config import logging
from src.logger import set_correlation_id
from src.metrics import RPSTrackerMiddleware
from src.storage.redis import setup_redis

logger = logging.getLogger('backend_logger')

@asynccontextmanager
async def lifespan(app: FastAPI):
    polling_task: asyncio.Task[None] | None = None
    wh_info = await bot.get_webhook_info()
    if settings.BOT_WEBHOOK_URL and wh_info != settings.BOT_WEBHOOK_URL:
        await bot.set_webhook(settings.BOT_WEBHOOK_URL)
    else:
        polling_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))

    yield

    if polling_task is not None:
        polling_task.cancel()
        try:
            await polling_task
        except asyncio.CancelledError:
            logger.info('Stop polling')

    await bot.delete_webhook()


def create_app() -> FastAPI:
    correlation_id = set_correlation_id()
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(router)
    app.add_middleware(RPSTrackerMiddleware)
    logger.info(f'Приложение создано [{correlation_id}]')
    return app




if __name__ == '__main__':
    uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8001, workers=1)
