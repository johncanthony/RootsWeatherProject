from fastapi import APIRouter
import logging
from google_auth_oauthlib.flow import InstalledAppFlow

log = logging.getLogger('uvicorn')
authRouter = APIRouter()

# Google API credentials
CLIENT_SECRETS_FILE = './creds/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


@authRouter.get('/auth', tags=['auth'])
async def auth():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = InstalledAppFlow.DEFAULT_AUTH_REDIRECT_URI
    auth_url, _ = flow.authorization_url(prompt='consent')
    return {'auth_url': auth_url}


@authRouter.get('/callback', tags=['auth'])
async def callback(code: str):
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    flow.redirect_uri = InstalledAppFlow.DEFAULT_AUTH_REDIRECT_URI
    flow.fetch_token(code=code)
    credentials = flow.credentials
    refresh_token = credentials.refresh_token
    access_token = credentials.token
    return {'refresh_token': refresh_token, 'access_token': access_token}
