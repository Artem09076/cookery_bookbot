from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router import router
from src.model.model import Recipe
from src.schema.recept import ReceptPost, ReceptResponse
from src.storage.db import get_db



@router.get('/receipts')
async def get_receipts(session: AsyncSession = Depends(get_db)):
    receipts = await session.execute(select(Recipe))
    res = []
    for recipe in receipts.all():
        res.append(recipe[0].__dict__)

    return {'receipts': res}

@router.post('/receipts', response_model=ReceptResponse)
async def create_recept(body: ReceptPost, session: AsyncSession = Depends(get_db)) -> ORJSONResponse:
    recept = Recipe(**body.dict())
    session.add(recept)
    await session.commit()
    return ORJSONResponse({'id': recept.id})


@router.get('/receipts/{user_id}')
async def get_recipe_by_user_id(user_id: int, session: AsyncSession = Depends(get_db)):
    receipts = await session.execute(select(Recipe).where(Recipe.user_id==user_id))
    res = []
    for receipt in receipts.all():
        res.append(receipt[0].__dict__)
    return {'receipts': res}
