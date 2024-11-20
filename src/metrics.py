import time
from asyncio import iscoroutinefunction
from functools import wraps
from typing import Callable

from prometheus_client import Histogram, Counter
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

BUCKETS = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    float('+inf'),
]

LATENCY = Histogram(
    'latency_seconds',
    'считает задержку',
    labelnames=['handler'],
    buckets=BUCKETS
)

def track_latency(func: Callable):
    @wraps(func)
    def sync_wrapper(*args, **kwargs):
        starts = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_time = time.monotonic() - starts
            LATENCY.labels(handler=func.__name__).observe(elapsed_time)


    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        starts = time.monotonic()
        try:
            return await func(*args, **kwargs)
        finally:
            elapsed_time = time.monotonic() - starts
            LATENCY.labels(func.__name__).observe(elapsed_time)


    return async_wrapper if iscoroutinefunction(func) else sync_wrapper

REQUESTS_TOTAL = Counter(
    'http_request_total',
    'Количество запросов на сервер',
    labelnames=['handler', 'status_code']
)

class RPSTrackerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        try:
            response: Response = await call_next(request)
            status_code = response.status_code
        except Exception:
            status_code = 500
            raise
        finally:
            REQUESTS_TOTAL.labels(
                handler=request.url.path,
                status_code=str(status_code)
            ).inc()

        return response

SEND_MESSAGE = Counter(
    'send_message_to_queue',
    'Отправленные сообщения в очередь',
)

