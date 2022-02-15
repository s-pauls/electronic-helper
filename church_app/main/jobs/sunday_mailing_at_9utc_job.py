import logging

from datetime import datetime, timedelta
from .job_base import JobBase
from ..core.utilities import datetime_helper
from ..core.viber.youtube_upcoming_broadcast_to_viber_event_handler import run_upcoming_broadcast_mailing_to_viber
from ..core.youtube.youtube_broadcast_wrapper import YouTubeBroadcastWrapper
from ..core.youtube.youtube_composer import YouTubeResourceComposer
from ..core.youtube.youtube_service import YouTubeService


class SundayMailingAt9utcJob(JobBase):

    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())
        self._logger = logging.getLogger(__name__)
        self._youtube_service = YouTubeService()

    def execute(self, parameters):
        youtube = YouTubeResourceComposer().compose()

        upcoming_live_broadcasts = self._youtube_service.get_upcoming_live_broadcast(youtube)

        if len(upcoming_live_broadcasts) == 0:
            self._logger.debug('No scheduled broadcasts')
            return

        for upcoming_live_broadcast in upcoming_live_broadcasts:
            upcoming_live_broadcast_wrapper = YouTubeBroadcastWrapper(upcoming_live_broadcast)

            if not upcoming_live_broadcast_wrapper.has_scheduled_start_time():
                continue

            scheduled_start_time_utc = upcoming_live_broadcast_wrapper.get_scheduled_start_time()
            now_utc = datetime_helper.now_with_utc_timezone()
            diff = scheduled_start_time_utc - now_utc
            diff_in_hours = diff.total_seconds() / 3600

            youtube_id = upcoming_live_broadcast_wrapper.get_id()

            if 0 < diff_in_hours <= 1:

                self._logger.debug(f'Broadcast {youtube_id} will be soon')

                # рассылка в вайбер
                run_upcoming_broadcast_mailing_to_viber(youtube_id,  schedule=timedelta(seconds=2))

                # рассылка в телеграм
                # todo

                # рассылка в VK
                # todo
            else:
                self._logger.debug(f'Broadcast {youtube_id} will be later')


def get_scheduled_start_time(elem) -> datetime:
    return YouTubeBroadcastWrapper(elem).get_scheduled_start_time()
