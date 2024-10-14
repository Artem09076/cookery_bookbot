import sys
import os
from src.logger import set_correlation_id
from src.log_config import logging

logger = logging.getLogger('backend_logger')

correlation_id = set_correlation_id()
logger.info(f"Логгер работает! [{correlation_id}]")
