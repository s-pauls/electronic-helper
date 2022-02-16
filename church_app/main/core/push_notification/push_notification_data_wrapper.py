class PushNotificationDataWrapper:
    def __init__(self, data):
        self._data: dict = data

    def get_app_name(self) -> str:
        return self._data.get('name')

    def get_pkg(self) -> str:
        return self._data.get('pkg')

    def get_title(self) -> str:
        return self._data.get('title')

    def get_text(self) -> str:
        return self._data.get('text')

    def get_user_name(self) -> str:
        return self._data.get('user')

    def get_subtext(self) -> str:
        return self._data.get('subtext')

    def get_big_text(self) -> str:
        return self._data.get('bigtext')

    def get_info_text(self) -> str:
        return self._data.get('infotext')
