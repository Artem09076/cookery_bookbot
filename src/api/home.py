from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.api.router import router
from src.storage.db import get_db


@router.get('/home/')
async def home(session: AsyncSession = Depends(get_db)) -> JSONResponse:
    return  ORJSONResponse({'massage': 'hello'})