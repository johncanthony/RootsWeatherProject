from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ManagerAPI.api.routers import jobs, auth

managerAPI = FastAPI()

origins = [
    "http://weather.memant.net",
    "https://weather.memant.net",
    "http://mac.memant.net",
    "https://mac.memant.net"
]

managerAPI.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@managerAPI.get('/health')
async def health():
    return {'managerAPI': 'up'}

'''
Include additional routers
'''
managerAPI.include_router(jobs.jobRouter)
managerAPI.include_router(auth.authRouter)
