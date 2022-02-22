import logging

from background_task import background
from .youtube_service import YouTubeService
from ..trello.trello_service import TrelloService
from ..utilities.handler_base import HandlerBase
from ..utilities import datetime_helper



# Отложенный запуск обработки начала трансляции (5 мин)
# https://django-background-tasks.readthedocs.io/en/latest/#creating-and-registering-tasks
@background(schedule=60)
def run_delayed_broadcast_ended(youtube_id: str):
    try:
        handler = YouTubeBroadcastEndedEventHandler()
        handler.handle(youtube_id)
    except Exception:
        # Exception was logged in HandlerBase
        # Если случается ошибка нам ненужно повторно выполнять эту задачу во избежания повторной рассылки!
        pass


"""
При окончании трансляции нужно создать карточки в Trello  
"""


class YouTubeBroadcastEndedEventHandler(HandlerBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._trello_service = TrelloService()
        self._youtube_service = YouTubeService()

    def execute(self, parameters):
        youtube_id = parameters

        self._logger.info(f'Broadcast {youtube_id} has ended')

        broadcast = self._youtube_service.get_live_broadcast_by_youtube_id_from_db(youtube_id)
        if not broadcast:
            self.logger.error(f'broadcast with youtube_id: {youtube_id} not found in database')
            return

        if datetime_helper.is_sunday(broadcast.scheduled_start_time):
            self._trello_service.create_new_preaching_card(
                youtube_title=broadcast.youtube_title,
                youtube_url=f'https://youtu.be/{broadcast.youtube_id}'
            )

            self._trello_service.create_update_youtube_description_card(
                youtube_title=broadcast.youtube_title,
                youtube_url=f'https://youtu.be/{broadcast.youtube_id}'
            )





