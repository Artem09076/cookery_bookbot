import logging.config
from contextvars import ContextVar
from uuid import uuid4

correlation_id_context: ContextVar[str] = ContextVar('correlation_id', default='N/A')


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.correlation_id = correlation_id_context.get()
        return super().format(record)


def set_correlation_id():
    correlation_id = str(uuid4())
    correlation_id_context.set(correlation_id)
    return correlation_id


logger = logging.getLogger('backend_logger')
