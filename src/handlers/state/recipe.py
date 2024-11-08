from aiogram.fsm.state import StatesGroup, State


class RecipeGroup(StatesGroup):
    recipe_title = State()
    ingredients = State()
    description_recipe = State()
    check_state = State()