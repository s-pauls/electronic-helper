import logging

from background_task import background

from .youtube_composer import YouTubeResourceComposer
from .youtube_service import YouTubeService
from ..utilities import datetime_helper
from ..utilities.handler_base import HandlerBase


# Отложенный запуск обработки начала трансляции
# https://django-background-tasks.readthedocs.io/en/latest/#creating-and-registering-tasks


@background(schedule=60)
def run_delayed_broadcast_started(youtube_id: str):
    handler = YouTubeBroadcastStartedEventHandler()
    handler.handle(youtube_id)


"""
При запуске новой трансляции нужно выслать сообщение в чат. 
Пригласить всех соединиться в духе
"""


class YouTubeBroadcastStartedEventHandler(HandlerBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._youtube_service = YouTubeService()

    def execute(self, parameters):

        youtube_id = parameters

        self._logger.info(f'Broadcast {youtube_id} has started')

        youtube = YouTubeResourceComposer().compose()

        broadcast = self._youtube_service.get_live_broadcast_by_youtube_id_from_db(youtube_id)

        if not broadcast:
            self._logger.error(f'broadcast with youtube_id: {youtube_id} not found in database')
            return

        if datetime_helper.is_sunday(broadcast.scheduled_start_time):

            # max 200 chars
            messages: [str] = [
                'Рады приветствовать Вас! '
                'Здорово, что мы будем славить нашего Бога вместе! ',

                'Нам будет приятно получить от Вас отзыв о служении в целом. '
                'Конструктивная критика поможет нам сделать наше служение качественнее. '
                'А положительные отзывы прибавляют нам сил и вдохновляют. ',

                'Если не хватает слов чтобы выразить Ваши ощущения - ставьте лайк 👍!',

                'Вы можете писать просьбы о поддержке в молитве 🙏 в этот чат. '
                'Ваши просьбы будут записаны в список молитвенных нужд.',

                'Приятного просмотра!',
            ]

            for message in messages:
                self._youtube_service.insert_live_chat_message(
                    youtube=youtube,
                    live_chat_id=broadcast.live_chat_id,
                    message_text=message
                )
