class YouTubeLiveChatMessagesWrapper:
    def __init__(self, live_chat_messages):
        self._live_chat_messages = live_chat_messages

    def get_messages(self) -> list:
        return list(self._live_chat_messages.get('items'))

    def get_next_page_token(self) -> str:
        return self._live_chat_messages.get('nextPageToken')

    def has_messages(self) -> bool:
        return len(self.get_messages()) > 0
