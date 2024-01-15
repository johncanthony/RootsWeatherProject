import uvicorn
from ManagerAPI import managerAPI

if __name__ == '__main__':
    config = uvicorn.Config(managerAPI, port=8000, log_level="info")
    server = uvicorn.Server(config)
    server.run()
