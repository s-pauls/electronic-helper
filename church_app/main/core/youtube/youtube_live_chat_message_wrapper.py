class YouTubeLiveChatMessageWrapper:
    def __init__(self, live_chat_message):
        self._live_chat_message = live_chat_message

    def get_message_id(self) -> str:
        return self._live_chat_message.get('id')

    def get_live_chat_id(self) -> str:
        return self._live_chat_message.get('snippet', {}).get('liveChatId')

    def get_message_text(self) -> str:
        # возможно, текст сообщение есть еще тут get('snippet', {}).get('displayMessage')
        return self._live_chat_message.get('snippet', {}).get('textMessageDetails', {}).get('messageText')

    def get_sender_name(self) -> str:
        return self._live_chat_message.get('authorDetails', {}).get('displayName')

    def get_sender_profile_image_url(self) -> str:
        return self._live_chat_message.get('authorDetails', {}).get('profileImageUrl')

    def is_sender_chat_owner(self) -> bool:
        return self._live_chat_message.get('authorDetails', {}).get('isChatOwner')

    def is_sender_chat_moderator(self) -> bool:
        return self._live_chat_message.get('authorDetails', {}).get('isChatModerator')
