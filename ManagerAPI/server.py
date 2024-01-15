import uvicorn
from ManagerAPI import managerAPI
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('Starting ManagerAPI')

if __name__ == '__main__':
    config = uvicorn.Config(managerAPI, port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
