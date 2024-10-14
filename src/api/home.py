from aiogram.types import Update
from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from starlette.requests import Request
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.router import router
from src.bot import get_dp, get_bot
from src.storage.db import get_db


@router.post('/home')
async def home(request: Request) -> None:
    data = await request.json()
    update = Update(**data)
    dp = get_dp()
    await dp.feed_webhook_update(get_bot(), update)
