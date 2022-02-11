from datetime import datetime


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
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
