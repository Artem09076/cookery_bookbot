from fastapi.params import Depends
from fastapi.responses import ORJSONResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.router import router
from src.model.model import Recipe
from src.schema.recipe import RecipePost, RecipeResponse
from src.storage.db import get_db
from src.logger import set_correlation_id, logger


@router.get('/receipts')
async def get_receipts(session: AsyncSession = Depends(get_db)):
    correlation_id = set_correlation_id()
    logger.info(f'Получение всех рецептов [correlation_id: {correlation_id}]')
    receipts = await session.execute(select(Recipe))
    res = []
    for recipe in receipts.all():
        res.append(recipe[0].__dict__)
    logger.info(f'Найдено рецептов: {len(res)} [correlation_id: {correlation_id}]')
    return {'receipts': res}

@router.post('/receipts', response_model=RecipeResponse)
async def create_recipe(body: RecipePost, session: AsyncSession = Depends(get_db)) -> ORJSONResponse:
    correlation_id = set_correlation_id()
    logger.info(f'Создание нового рецепта [correlation_id: {correlation_id}, recipe_title: {body.recipe_title}]')
    recipe = Recipe(**body.model_dump())
    session.add(recipe)
    await session.commit()
    logger.info(f'Рецепт создан с ID: {recipe.id} [correlation_id: {correlation_id}]')
    return ORJSONResponse({'id': recipe.id})


@router.get('/receipts/{user_id}')
async def get_recipe_by_user_id(user_id: int, session: AsyncSession = Depends(get_db)):
    correlation_id = set_correlation_id()
    logger.info(f'Получение рецептов для пользователя ID: {user_id} [correlation_id: {correlation_id}]')
    receipts = await session.execute(select(Recipe).where(Recipe.user_id==user_id))
    res = []
    for recipe in receipts.all():
        res.append(recipe[0].__dict__)
    logger.info(f'Найдено рецептов для пользователя ID {user_id}: {len(res)} [correlation_id: {correlation_id}]')
    return {'receipts': res}
