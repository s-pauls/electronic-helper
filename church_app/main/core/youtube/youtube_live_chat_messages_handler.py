import logging

from .youtube_composer import YouTubeResourceComposer
from .youtube_live_chat_message_wrapper import YouTubeLiveChatMessageWrapper
from .youtube_service import YouTubeService
from ..prayer_need.prayer_need_service import PrayerNeedService
from ..utilities import datetime_helper
from ..utilities.handler_base import HandlerBase
from ..wording.wording_service import WordingService

"""
В этот обработчик приходят паки сообщений.
Периодически идет опрос новых сообщений в чате и если появились новые сообщения с момента последнего опроса,
то они передаются этому обработчику  
"""


class YouTubeLiveChatMessagesHandler(HandlerBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._youtube_service = YouTubeService()
        self._wording_service = WordingService()

    def execute(self, parameters):
        youtube_id = parameters.get('youtube_id')
        messages = list(parameters.get('messages'))

        if not youtube_id:
            self._logger.error('youtube_id is not set')
            return

        if not messages:
            self._logger.info('messages list is empty')
            return

        broadcast = self._youtube_service.get_live_broadcast_by_youtube_id_from_db(youtube_id)

        if not broadcast:
            self._logger.error(f'broadcast with youtube_id: {youtube_id} not found in database')
            return

        if datetime_helper.is_sunday(broadcast.scheduled_start_time):
            self._logger.info(f'{broadcast.youtube_id} is Sunday broadcast. New Message\'s batch is processing...')
            self.process_sunday_messages(messages, broadcast.live_chat_id)

        else:
            self._logger.info(f'{broadcast.youtube_id} is not Sunday broadcast')

    def process_sunday_messages(self, messages, live_chat_id: str):
        prayer_nees_service = PrayerNeedService()
        for message in messages:

            message_wrapper = YouTubeLiveChatMessageWrapper(message)

            if message_wrapper.is_sender_chat_owner() or message_wrapper.is_sender_chat_moderator():
                return

            sent = prayer_nees_service.process_message(
                sender_name=message_wrapper.get_sender_name(),
                message_text=message_wrapper.get_message_text(),
                message_source='youtube'
            )

            if sent:
                youtube = YouTubeResourceComposer().compose()
                self._youtube_service.insert_live_chat_message(
                    youtube=youtube,
                    live_chat_id=live_chat_id,
                    message_text=self._wording_service.get_your_prayer_need_is_saved_wording(message_wrapper.get_sender_name())
                )
