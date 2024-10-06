from pydantic import BaseModel



class ReceptPost(BaseModel):
    recipe_title: str
    ingredients: list[str]
    likes: int = 0
    dislikes: int =0
    user_id: int

class ReceptResponse(BaseModel):
    id: str