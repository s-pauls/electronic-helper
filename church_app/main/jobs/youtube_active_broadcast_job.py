import logging
import os

from ..core.youtube.youtube_broadcast_wrapper import YouTubeBroadcastWrapper
from ..core.youtube.youtube_builder import YouTubeResourceComposer
from ..core.youtube.youtube_live_chat_messages_wrapper import YouTubeLiveChatMessagesWrapper
from ..core.youtube.youtube_service import YouTubeService
from ..core.youtube.youtube_user_info_builder import YouTubeUserInfoBuilder
from .job_base import JobBase


class YouTubeActiveBroadcastJob(JobBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())

    def execute(self, parameters):
        logger = logging.getLogger(__name__)

        user_info_builder = YouTubeUserInfoBuilder()
        user_info_builder.set(
            refresh_token=os.getenv('YOUTUBE_REFRESH_TOKEN'),
            client_id=os.getenv('YOUTUBE_CLIENT_ID'),
            client_secret=os.getenv('YOUTUBE_CLIENT_SECRET'),
        )

        user_info = user_info_builder.user_info

        if not user_info.get('refresh_token'):
            logger.info('YouTube\'s environment variables is not set ')
            return

        youtube = YouTubeResourceComposer(user_info).compose()
        youtube_service = YouTubeService()

        active_live_broadcast = youtube_service.get_active_live_broadcast(youtube)

        if not active_live_broadcast:
            logger.info('No active broadcast')
            return

        broadcast_wrapper = YouTubeBroadcastWrapper(active_live_broadcast)

        logger.info(f"Current broadcast {broadcast_wrapper.get_title()}")

        live_chat_messages = youtube_service.get_live_chat_messages(youtube, broadcast_wrapper.get_live_chat_id())

        live_chat_messages_wrapper = YouTubeLiveChatMessagesWrapper(live_chat_messages)

        if not live_chat_messages_wrapper.has_messages():
            logger.info('No messages')
            return
