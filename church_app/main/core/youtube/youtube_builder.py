import googleapiclient.discovery
import googleapiclient.errors
import os

from google.oauth2.credentials import Credentials
from django.conf import settings

class YouTubeResourceComposer:

    def __init__(self, user_info):
        # Disable OAuth lib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        if settings.DEBUG:
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self._user_info = user_info

    def compose(self):
        api_service_name = "youtube"
        api_version = "v3"

        credentials = Credentials.from_authorized_user_info(self._user_info)
        youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube
