import logging as log
from logging.handlers import TimedRotatingFileHandler
from dataclasses import dataclass
import os


@dataclass
class LogHandler:

    service_name: str = 'running'

    def __post_init__(self):
        self.dir: str = os.getenv('RWP_LOG_DIR', './')
        self.level: str = os.getenv('RWP_LOG_LEVEL', 'INFO')

    def bootstrap(self):

        logger = log.getLogger()
        logger.setLevel(getattr(log, self.level))
        formatter = log.Formatter(
            '%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
            '%b %d %H:%M:%S')
        handler = TimedRotatingFileHandler(f'{self.dir}/{self.service_name}-service.log', when='midnight', interval=1, backupCount=5)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        log.info(f'[Log Bootstrap] Logging DIR set to {os.getenv("RWP_LOG_DIR", "not set")}')
        log.info(f'[Log Bootstrap] Logging to {self.dir}/{self.service_name}-service.log')
