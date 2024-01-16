import logging as log
from logging.handlers import TimedRotatingFileHandler
from dataclasses import dataclass


@dataclass
class LogHandler:

    service_name: str = 'running'
    level: str = 'INFO'

    def bootstrap(self):

        logger = log.getLogger()
        logger.setLevel(getattr(log, self.level))
        formatter = log.Formatter(
            '%(asctime)s [%(levelname)s] [%(module)s] %(message)s',
            '%b %d %H:%M:%S')
        handler = TimedRotatingFileHandler(f'logs/{self.service_name}-service.log', when='midnight', interval=1, backupCount=5)

        handler.setFormatter(formatter)
        logger.addHandler(handler)
