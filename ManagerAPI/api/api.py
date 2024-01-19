from fastapi import FastAPI
from ManagerAPI.api.routers import jobs, auth

managerAPI = FastAPI()


@managerAPI.get('/health')
async def health():
    return {'managerAPI': 'up'}

'''
Include additional routers
'''
managerAPI.include_router(jobs.jobRouter)
managerAPI.include_router(auth.authRouter)
