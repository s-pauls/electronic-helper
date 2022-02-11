
class YouTubeUserInfoBuilder:
    def __init__(self):
        self._user_info: dict = {}
        self.reset()

    def reset(self) -> None:
        self._user_info = dict(refresh_token='', client_id='', client_secret='')

    @property
    def user_info(self):
        user_info = self._user_info
        self.reset()
        return user_info

    def set(self, refresh_token: str, client_id: str, client_secret: str) -> None:
        self._user_info['refresh_token'] = refresh_token
        self._user_info['client_id'] = client_id
        self._user_info['client_secret'] = client_secret
