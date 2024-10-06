from pydantic import BaseModel


class AuthPost(BaseModel):
    user_id: int

class AuthResponse(BaseModel):
    token: str