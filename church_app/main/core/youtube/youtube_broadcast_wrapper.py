from datetime import datetime

from ..utilities import datetime_helper

PRIVACY_STATUS_PUBLIC = 'public'
PRIVACY_STATUS_UNLISTED = 'unlisted'


class YouTubeBroadcastWrapper:
    def __init__(self, broadcast):
        self._broadcast = broadcast

    def get_id(self) -> str:
        return self._broadcast.get('id')

    def get_live_chat_id(self) -> str:
        return self._broadcast.get('snippet', {}).get('liveChatId')

    def get_title(self) -> str:
        return self._broadcast.get('snippet', {}).get('title')

    def get_scheduled_start_time(self) -> datetime:
        date_str = self._broadcast.get('snippet', {}).get('scheduledStartTime')
        return datetime_helper.youtube_datetime_to_datetime(date_str)

    def has_scheduled_start_time(self) -> bool:
        date_str = self._broadcast.get('snippet', {}).get('scheduledStartTime')
        return date_str

    # public
    # unlisted - доступ по ссылке
    def get_privacy_status(self) -> str:
        return self._broadcast.get('status', {}).get('privacyStatus')
