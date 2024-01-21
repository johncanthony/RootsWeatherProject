import uvicorn
from ManagerAPI import managerAPI
import os

HOSTNAME = os.getenv('MANAGERAPI_HOSTNAME') or 'localhost'
PORT = int(os.getenv('MANAGERAPI_PORT')) or 8000


def launch():
    config = uvicorn.Config(managerAPI, host=HOSTNAME, port=PORT, log_level="info", log_config="log.ini")
    server = uvicorn.Server(config)
    server.run()


if __name__ == '__main__':
    launch()
