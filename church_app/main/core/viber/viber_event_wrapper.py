class ViberEventWrapper:
    def __init__(self, event_data):
        self._event_data: dict = event_data

    def get_event_name(self) -> str:
        return self._event_data['event']

    def get_message_token(self) -> str:
        return self._event_data['message_token']

    def get_sender_id(self) -> str:
        return self._event_data.get('sender', {}).get('id')

    def get_sender_name(self) -> str:
        return self._event_data.get('sender', {}).get('name')

    def get_sender_avatar(self) -> str:
        return self._event_data.get('sender', {}).get('avatar')

    def get_message_type(self) -> str:
        return self._event_data.get('message', {}).get('type')

    def get_message_text(self) -> str:
        return self._event_data.get('message', {}).get('text')
