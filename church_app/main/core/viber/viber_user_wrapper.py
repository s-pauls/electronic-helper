class ViberUserWrapper:
    def __init__(self, user):
        self._user: dict = user

    def get_user_id(self) -> str:
        return self._user.get('id')

    def get_user_name(self) -> str:
        return self._user.get('name')

    def get_user_avatar(self) -> str:
        return self._user.get('avatar')

    def get_user_language(self) -> str:
        return self._user.get('language')

    def get_user_country(self) -> str:
        return self._user.get('country')
