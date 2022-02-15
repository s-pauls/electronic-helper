import logging

from background_task import background
from .viber_service import ViberService
from ..youtube.youtube_service import YouTubeService
from ..utilities.handler_base import HandlerBase


# Отложенный запуск обработки начала трансляции
# https://django-background-tasks.readthedocs.io/en/latest/#creating-and-registering-tasks
@background(schedule=60)
def run_upcoming_broadcast_mailing_to_viber(youtube_id: str):
    handler = YouTubeUpcomingBroadcastToViberEventHandler()
    handler.handle(youtube_id)


"""
Скоро начнется трансляция   
"""


class YouTubeUpcomingBroadcastToViberEventHandler(HandlerBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._youtube_service = YouTubeService()
        self._viber_service = ViberService()

    def execute(self, parameters):
        youtube_id = parameters

        self._logger.debug(f'Start mailing to Viber about upcoming broadcast {youtube_id}')

        message_text = 'Наступил этот день воскресенья!\r\n' \
                       'Предавай все дела забвенью!\r\n' \
                       'Подключись, чтобы услышать слово!\r\n' \
                       '\r\n' \
                       'Трансляция в 10:00:\r\n' \
                       f'https://youtu.be/{youtube_id}'

        self._viber_service.send_text_message_to_all_subscribers(message_text)







