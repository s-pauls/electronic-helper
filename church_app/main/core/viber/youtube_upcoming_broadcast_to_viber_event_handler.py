import logging

from background_task import background
from .viber_service import ViberService
from ..utilities import datetime_helper
from ..wording.wording_service import WordingService
from ..youtube.youtube_broadcast_wrapper import PRIVACY_STATUS_PUBLIC
from ..youtube.youtube_service import YouTubeService
from ..utilities.handler_base import HandlerBase


# Отложенный запуск обработки начала трансляции
# https://django-background-tasks.readthedocs.io/en/latest/#creating-and-registering-tasks
@background(schedule=60)
def run_upcoming_broadcast_mailing_to_viber(parameters):
    handler = YouTubeUpcomingBroadcastToViberEventHandler()
    handler.handle(parameters)


"""
Скоро начнется трансляция   
"""


class YouTubeUpcomingBroadcastToViberEventHandler(HandlerBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._youtube_service = YouTubeService()
        self._viber_service = ViberService()
        self._wording_service = WordingService()

    def execute(self, parameters):
        youtube_id = parameters['youtube_id']
        title = parameters.get('title')
        privacy_status = parameters.get('privacy_status')
        scheduled_start_time = datetime_helper.str_isoformat_to_datetime(parameters.get('scheduled_start_time'))

        self._logger.debug(f'Start mailing to Viber about upcoming broadcast {youtube_id}')

        message_text = self._wording_service.get_youtube_live_broadcast_wording(
            youtube_id=youtube_id,
            title=title,
            scheduled_start_time=scheduled_start_time)

        if privacy_status == PRIVACY_STATUS_PUBLIC:
            self._viber_service.send_text_message_to_subscribers(
                message_text=message_text,
                role='*'
                )
        else:
            self._viber_service.send_text_message_to_subscribers(
                message_text=message_text,
                role='manager'
            )
