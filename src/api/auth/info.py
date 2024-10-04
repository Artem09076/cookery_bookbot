from fastapi.responses import ORJSONResponse

from src.api.router import router
from src.schema.login import AuthResponse


@router.get('/info', response_model=AuthResponse)
def get_info(token: str):
    return ORJSONResponse(token)