import logging
import logging.config
import yaml

with open('config/logging.conf.yml', 'r') as f:
    LOGGING_CONFIG = yaml.full_load(f)

logging.config.dictConfig(LOGGING_CONFIG)
