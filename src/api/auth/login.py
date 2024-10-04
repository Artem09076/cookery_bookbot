from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router import router
from src.schema.login import AuthResponse, AuthPost
from src.storage.db import get_db
from src.model.model import User

@router.post('/login', response_model=AuthResponse)
def login(body: AuthPost, session: AsyncSession = Depends(get_db)):
    user = User()