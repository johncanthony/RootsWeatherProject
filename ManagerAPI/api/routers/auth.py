from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from ManagerAPI.api.managers.connection_manager import AuthManager, RedisConnectionConfig
import logging
import google_auth_oauthlib.flow
import os


log = logging.getLogger('uvicorn')
authRouter = APIRouter()

session = {}

# Google API credentials
CLIENT_SECRETS_FILE = os.getenv('CLIENT_SECRETS_FILE') or 'client_secrets.json'
FLOW_BASE_URI = os.getenv('FLOW_BASE_URI') or 'localhost'
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']


@authRouter.get("/auth")
async def auth_init():

    log.info('Initializing auth')
    """Initialize auth and redirect"""
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES
    )

    flow.redirect_uri = f'https://{FLOW_BASE_URI}/callback'

    log.info(f'Fetching authorization url - {flow.redirect_uri}')
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )

    session['state'] = state

    return RedirectResponse(authorization_url)


@authRouter.get("/callback")
async def auth_callback(request: Request):

    log.info('[Callback] Auth')
    """Verify login"""
    state = session['state']

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        state=state
    )

    flow.redirect_uri = f'https://{FLOW_BASE_URI}/callback'
    authorization_response = f'https://{FLOW_BASE_URI}{request.url.path}?{request.url.query}'
    log.debug(f'[Callback] Authorization Response: {authorization_response}')

    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    AuthManager(refresh_token=credentials.refresh_token, connection_config=RedisConnectionConfig()).store()

    return RedirectResponse(url=f'https://{FLOW_BASE_URI}/')


@authRouter.get("/refresh_token")
async def refresh_token():

    log.info('Refreshing token')

    return AuthManager(connection_config=RedisConnectionConfig()).fetch()
