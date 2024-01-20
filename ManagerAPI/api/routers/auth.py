from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
import logging
import json
import google_auth_oauthlib.flow


log = logging.getLogger('uvicorn')
authRouter = APIRouter()

session = {}

# Google API credentials
CLIENT_SECRETS_FILE = './creds/client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


@authRouter.get("/auth")
async def auth_init():
    """Initialize auth and redirect"""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = 'https://mroots.io/callback'

    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    session['state'] = state

    return RedirectResponse(authorization_url)


@authRouter.get("/callback")
async def auth_callback(request: Request):
    """Verify login"""
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = 'https://mroots.io/callback'
    authorization_response = f'https://mroots.io/{request.url.path}'

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    return {'credentials': f'{credentials.refresh_token}'}
