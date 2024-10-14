import logging.config
from contextlib import suppress
import yaml
from uuid import uuid4
from contextvars import ContextVar

correlation_id_context: ContextVar[str] = ContextVar(
    'correlation_id', default='N/A')

# with open('config/logging.conf.yml', 'r') as f:
#     LOGGING_CONFIG = yaml.safe_load(f)

# logging.config.dictConfig(LOGGING_CONFIG)


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        record.correlation_id = correlation_id_context.get()
        return super().format(record)


def set_correlation_id():
    correlation_id = str(uuid4())
    correlation_id_context.set(correlation_id)
    return correlation_id


logger = logging.getLogger('backend_logger')
