from fastapi import APIRouter
import logging

log = logging.getLogger('uvicorn')
authRouter = APIRouter()


@authRouter.get('/auth', tags=['auth'])
async def auth():
    return {'auth': 'up'}


@authRouter.get('/callback', tags=['auth'])
async def callback():
    return {'callback': 'up'}
