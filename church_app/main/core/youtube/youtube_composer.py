import googleapiclient.discovery
import googleapiclient.errors
import os

from django.conf import settings
from google.oauth2.credentials import Credentials
from .youtube_user_info_builder import YouTubeUserInfoBuilder


class YouTubeResourceComposer:

    def __init__(self):
        # Disable OAuth lib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        if settings.DEBUG:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def compose(self):
        api_service_name = "youtube"
        api_version = "v3"

        user_info = self.get_user_info()

        credentials = Credentials.from_authorized_user_info(user_info)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube

    def get_user_info(self):
        user_info_builder = YouTubeUserInfoBuilder()
        user_info_builder.set(
            refresh_token=os.getenv('YOUTUBE_REFRESH_TOKEN'),
            client_id=os.getenv('YOUTUBE_CLIENT_ID'),
            client_secret=os.getenv('YOUTUBE_CLIENT_SECRET'),
        )

        user_info = user_info_builder.user_info

        if not user_info.get('refresh_token'):
            raise ValueError('YouTube\'s environment variables is not set ')

        return user_info
