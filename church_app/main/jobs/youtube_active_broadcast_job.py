import logging
from datetime import timedelta

from ..core.youtube.youtube_broadcast_ended_event_handler import run_delayed_broadcast_ended
from ..core.youtube.youtube_broadcast_started_event_handler import run_delayed_broadcast_started
from ..core.youtube.youtube_broadcast_wrapper import YouTubeBroadcastWrapper
from ..core.youtube.youtube_composer import YouTubeResourceComposer
from ..core.youtube.youtube_live_chat_messages_handler import YouTubeLiveChatMessagesHandler
from ..core.youtube.youtube_live_chat_messages_wrapper import YouTubeLiveChatMessagesWrapper
from ..core.youtube.youtube_service import YouTubeService
from .job_base import JobBase


"""
Эта джоба выполняется каждую минуту.
Ее задачи 
- определить, что началась новая трансляция и зафиксировать это в базе
- определить, что трансляция закончилась и зафиксировать это в базе
- вычитывать новые сообщения из чата и отправлять на дальнейшую обработку 
"""


class YouTubeActiveBroadcastJob(JobBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._youtube_service = YouTubeService()

    def execute(self, parameters):
        youtube = YouTubeResourceComposer().compose()

        active_live_broadcast = self._youtube_service.get_active_live_broadcast(youtube)
        active_live_broadcast_wrapper = YouTubeBroadcastWrapper(active_live_broadcast)

        active_live_broadcast_in_db = self._youtube_service.get_active_live_broadcast_from_db()

        if not active_live_broadcast:
            self._logger.debug('No active broadcast')

            if active_live_broadcast_in_db:
                self._logger.debug(f"Live broadcast {active_live_broadcast_in_db.youtube_id} finished")

                self._youtube_service.set_live_broadcast_finished(active_live_broadcast_in_db.youtube_id)

                # отложенный запуск обработки окончания трансляции
                run_delayed_broadcast_ended(active_live_broadcast_in_db.youtube_id, schedule=timedelta(minutes=2))

                return

            return

        if not active_live_broadcast_in_db:
            self._logger.debug(f"New live broadcast {active_live_broadcast_wrapper.get_id()} started")

            self._youtube_service.add_new_live_broadcast_in_db(
                youtube_id=active_live_broadcast_wrapper.get_id(),
                youtube_title=active_live_broadcast_wrapper.get_title(),
                live_chat_id=active_live_broadcast_wrapper.get_live_chat_id(),
                scheduled_start_time=active_live_broadcast_wrapper.get_scheduled_start_time()
            )

            # отложенный запуск обработки начала трансляции
            run_delayed_broadcast_started(active_live_broadcast_wrapper.get_id(),  schedule=timedelta(minutes=5))

            return

        live_chat_messages = self._youtube_service.get_live_chat_messages(
            youtube=youtube,
            live_chat_id=active_live_broadcast_wrapper.get_live_chat_id(),
            page_token=active_live_broadcast_in_db.live_chat_next_page_token
        )

        live_chat_messages_wrapper = YouTubeLiveChatMessagesWrapper(live_chat_messages)

        self._youtube_service.set_live_broadcast_page_token(
            youtube_id=active_live_broadcast_wrapper.get_id(),
            page_token=live_chat_messages_wrapper.get_next_page_token()
        )

        if not live_chat_messages_wrapper.has_messages():
            self._logger.debug('No messages')
            return

        messages_handler = YouTubeLiveChatMessagesHandler()
        messages_handler.handle({
            'youtube_id': active_live_broadcast_wrapper.get_id(),
            'messages': live_chat_messages_wrapper.get_messages()
        })
