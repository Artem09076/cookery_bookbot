import asyncio
import random
import time

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from src.api.router import router
from src.metrics import LATENCY, track_latency


@router.get("/send")
@track_latency('test')
async def send(
    request: Request,
) -> Response:
    text = '_'.join([str(random.randint(0, 100)) for _ in range(10)])
    time.sleep(0.5)
    return Response()
