class ViberEventWrapper:
    def __init__(self, event_data):
        self._event_data: dict = event_data

    def get_event_name(self) -> str:
        return self._event_data['event']
