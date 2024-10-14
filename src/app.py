from contextlib import asynccontextmanager

import uvicorn
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI
from sqlalchemy.util import await_only

from config.settings import settings
from script.init_db import init_models
from src.api.login import router
from src.bot import setup_dp, setup_bot
from src.storage.redis import setup_redis
from src.logger import set_correlation_id
from src.log_config import logging 
from src.handlers.command.router import router as command_router

logger = logging.getLogger('backend_logger')

async def lifespan(app: FastAPI):
    dp = Dispatcher()
    dp.include_router(command_router)
    setup_dp(dp)
    bot = Bot(settings.BOT_TOKEN)
    setup_bot(bot)

    await  bot.set_webhook(settings.BOT_WEBHOOK_URL)
    yield
    await bot.delete_webhook()



def create_app() -> FastAPI:
    correlation_id = set_correlation_id()
    app = FastAPI(docs_url='/swagger', lifespan=lifespan)
    app.include_router(router)
    logger.info(f'Create app [{correlation_id}]')
    return  app

async def start_polling():
    redis = setup_redis()
    storage = RedisStorage(redis)

    dp = Dispatcher(storage=storage)
    setup_dp(dp)

    dp.include_router(command_router)

    bot = Bot(settings.BOT_TOKEN)
    setup_bot(bot)

    await bot.delete_webhook()
    await dp.start_polling(bot)




if __name__ == '__main__':
    # asyncio.run(init_models())
    if settings.BOT_WEBHOOK_URL:
        uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
    else:
        asyncio.run(start_polling())

