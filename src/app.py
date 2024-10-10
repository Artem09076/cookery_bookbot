import uvicorn
import asyncio
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from fastapi import FastAPI

from config.settings import settings
from src.api.login import router
from src.bot import setup_dp, setup_bot
from src.storage.redis import setup_redis


def create_app() -> FastAPI:
    app = FastAPI(docs_url='/swagger')
    app.include_router(router)
    return  app

async def start_polling():
    redis = setup_redis()
    storage = RedisStorage(redis)

    dp = Dispatcher(storage=storage)
    setup_dp(dp)



    bot = Bot(settings.BOT_TOKEN)
    setup_bot(bot)



    await dp.start_polling(bot)




if __name__ == '__main__':
    # uvicorn.run('src.app:create_app', factory=True, host='0.0.0.0', port=8000, workers=1)
    asyncio.run(start_polling())

