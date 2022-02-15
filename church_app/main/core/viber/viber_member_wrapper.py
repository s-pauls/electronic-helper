class ViberMemberWrapper:
    def __init__(self, info):
        self._info: dict = info

    def get_member_id(self) -> str:
        return self._info['id']

    def get_member_name(self) -> str:
        return self._info['name']

    def get_member_avatar(self) -> str:
        return self._info['avatar']

    def get_member_role(self) -> str:
        return self._info['role']
