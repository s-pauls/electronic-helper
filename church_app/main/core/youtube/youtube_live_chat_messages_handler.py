import logging

from .youtube_live_chat_message_wrapper import YouTubeLiveChatMessageWrapper
from .youtube_service import YouTubeService
from ..prayer_need.prayer_need_service import PrayerNeedService
from ..utilities.handler_base import HandlerBase

SUNDAY = 7

"""
В этот обработчик приходят паки сообщений.
Периодически идет опрос новых сообщений в чате и если появились новые сообщения с момента последнего опроса,
то они передаются этому обработчику  
"""


class YouTubeLiveChatMessagesHandler(HandlerBase):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        super().__init__(self.__class__.__name__.__str__())

    def execute(self, parameters):
        youtube_id = parameters.get('youtube_id')
        messages = list(parameters.get('messages'))

        if not youtube_id:
            self.logger.error('youtube_id is not set')
            return

        if not messages:
            self.logger.info('messages list is empty')
            return

        youtube_service = YouTubeService()
        broadcast = youtube_service.get_live_broadcast_by_youtube_id_from_db(youtube_id)

        if not broadcast:
            self.logger.error(f'broadcast with youtube_id: {youtube_id} not found in database')
            return

        if broadcast.scheduled_start_time.isoweekday() == SUNDAY:
            self.logger.info(f'{broadcast.youtube_id} is Sunday broadcast. New Message\'s batch is processing...')
            self.process_sunday_messages(messages)

        else:
            self.logger.info(f'{broadcast.youtube_id} is not Sunday broadcast')

    def process_sunday_messages(self, messages):
        prayer_nees_service = PrayerNeedService()
        for message in messages:

            message_wrapper = YouTubeLiveChatMessageWrapper(message)

            if message_wrapper.is_sender_chat_owner() or message_wrapper.is_sender_chat_moderator():
                return

            prayer_nees_service.process_message(
                sender_name=message_wrapper.get_sender_name(),
                message_text=message_wrapper.get_message_text(),
                message_source='youtube'
            )
