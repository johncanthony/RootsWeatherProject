from fastapi import APIRouter, Request
import logging
import json
from fastapi_sso.sso.google import GoogleSSO

log = logging.getLogger('uvicorn')
authRouter = APIRouter()

# Google API credentials
CLIENT_SECRETS_FILE = './creds/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

with open(CLIENT_SECRETS_FILE, 'r') as f:
    creds = json.load(f)

sso = GoogleSSO(
    client_id=creds['web']['client_id'],
    client_secret=creds['web']['client_secret'],
    redirect_uri="https://mroots.io/callback",
    allow_insecure_http=True,
    scope=SCOPES,
)


@authRouter.get("/auth")
async def auth_init():
    """Initialize auth and redirect"""
    with sso:
        return await sso.get_login_redirect(params={"prompt": "consent", "access_type": "offline"})


@authRouter.get("/auth/callback")
async def auth_callback(request: Request):
    """Verify login"""
    with sso:
        user = await sso.verify_and_process(request)
    return user
