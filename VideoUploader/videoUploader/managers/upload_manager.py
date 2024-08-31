from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import google.oauth2.credentials
from dataclasses import dataclass
import os
import json
import requests
import logging as log


@dataclass
class YTAuthManager:

    client_id: str = ""
    client_secret: str = ""
    token_url: str = "https://oauth2.googleapis.com/token"
    access_token: str = ""
    refresh_token: str = ""

    youtube_api_service_name: str = "youtube"
    youtube_api_version: str = "v3"

    @property
    def secrets_file(self):
        return os.getenv("CLIENT_SECRETS_FILE", "client_secrets.json")

    @property
    def manager_url(self):
        return os.getenv("MANAGER_URL", "localhost:8000")

    def fetch_refresh_token(self):

        try:
            log.debug(f'[VideoAuthManager] fetching refresh token from {self.manager_url}/refresh_token')
            refresh_token = requests.get(f'http://{self.manager_url}/refresh_token').json()
        except requests.exceptions.ConnectionError:
            return False
        except requests.exceptions.ReadTimeout:
            return False

        log.debug(f'[VideoAuthManager] fetched refresh token {refresh_token}')

        self.refresh_token = refresh_token['refresh_token']

        return True

    def pull_secrets(self):

        with open(self.secrets_file) as f:
            secrets = json.load(f)

        self.client_id = secrets["web"]["client_id"]
        self.client_secret = secrets["web"]["client_secret"]
        self.token_url = secrets["web"]["token_uri"]

        log.debug(f'[VideoAuthManager] pulled secrets {self.client_id} {self.client_secret} {self.token_url}')
        return True

    def fetch_credentials(self):

        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }

        try:
            access_token_response = requests.post(self.token_url, params=params)
        except requests.exceptions.ConnectionError:
            return False

        log.debug(f'[VideoAuthManager] fetched credentials {access_token_response.json()}')

        return google.oauth2.credentials.Credentials(access_token_response.json()['access_token'])

    def bootstrap(self):

        if not self.client_id:
            self.pull_secrets()

        if not self.refresh_token:
            self.fetch_refresh_token()

        return self


@dataclass
class YTVideoManager:

    title: str = ""
    description: str = ""
    video_type: str = ""
    privacy_status: str = "private"
    video_file: str = ""
    auth_manager: YTAuthManager = None

    def upload_video(self, credentials):

        if self.video_type == "shorts":
            self.description += "\n #Shorts"

        try:
            youtube = build(
                self.auth_manager.youtube_api_service_name,
                self.auth_manager.youtube_api_version,
                credentials=credentials
            )

            video = youtube.videos().insert(
                part="snippet,status",
                body={
                      "snippet": {
                         "title": self.title,
                         "description": self.description,
                      },
                      "status": {
                         "privacyStatus": self.privacy_status
                      }
                },
                media_body=MediaFileUpload(self.video_file, chunksize=-1, resumable=True)
            ).execute()

        except HttpError as e:
            log.error(f'Video Upload error - {e.resp.status} occurred: {e.content}')
            return False

        return video['id'] if "id" in video else False
