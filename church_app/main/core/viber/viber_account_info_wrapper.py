class ViberAccountInfoWrapper:
    def __init__(self, info):
        self._info: dict = info

    def get_status_message(self) -> str:
        return self._info['status_message']

    def get_subscribers_count(self) -> int:
        count_str = self._info['subscribers_count']
        return int(count_str)

    def get_members(self) -> list:
        members = self._info.get('members')
        return list(members)
