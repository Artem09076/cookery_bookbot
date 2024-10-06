from pydantic import BaseModel



class RecipePost(BaseModel):
    recipe_title: str
    ingredients: list[str]
    likes: int = 0
    dislikes: int =0
    user_id: int

class RecipeResponse(BaseModel):
    id: str