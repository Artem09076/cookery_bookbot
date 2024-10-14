from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router import router
from src.schema.login import AuthResponse, AuthPost
from src.storage.db import get_db
from src.model.model import User

@router.post('/login', response_model=AuthResponse)
async def login(body: AuthPost, session: AsyncSession = Depends(get_db)):
    user = User(user_id=body.user_id)
    session.add(user)
    await session.commit()
    return ORJSONResponse({'message': 'user add'}, 200)

