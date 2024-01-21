import logging as log
from logging.handlers import TimedRotatingFileHandler
from dataclasses import dataclass
import os

LOG_DIR = os.getenv('RWP_LOG_DIR') or './'
LOG_LEVEL = os.getenv('RWP_LOG_LEVEL') or 'INFO'


@dataclass
class LogHandler:

    service_name: str = 'running'
    dir: str = LOG_DIR
    level: str = LOG_LEVEL

    def bootstrap(self):

        logger = log.getLogger()
        logger.setLevel(getattr(log, self.level))
        formatter = log.Formatter(
            '%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
            '%b %d %H:%M:%S')
        handler = TimedRotatingFileHandler(f'{self.dir}{self.service_name}-service.log', when='midnight', interval=1, backupCount=5)

        handler.setFormatter(formatter)
        logger.addHandler(handler)
