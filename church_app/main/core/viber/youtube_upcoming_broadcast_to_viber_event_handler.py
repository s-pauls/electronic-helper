import logging

from background_task import background
from ..youtube.youtube_service import YouTubeService
from ..utilities.handler_base import HandlerBase


# Отложенный запуск обработки начала трансляции
# https://django-background-tasks.readthedocs.io/en/latest/#creating-and-registering-tasks
@background(schedule=2)
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

    def execute(self, parameters):
        youtube_id = parameters

        self._logger.debug(f'Start mailing to Viber about upcoming broadcast {youtube_id}')







