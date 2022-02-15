import os

from .viber_account_info_wrapper import ViberAccountInfoWrapper
from .viber_client import ViberClient
from .viber_member_wrapper import ViberMemberWrapper


class ViberService:

    def send_text_message(self, receiver_id: str, message_text: str):
        viber_client = self._get_viber_client()
        viber_client.send_text_message(receiver_id, message_text)

    def send_text_message_to_all_subscribers(self, message_text: str):
        viber_client = self._get_viber_client()

        account_info = viber_client.get_account_info()
        account_info_wrapper = ViberAccountInfoWrapper(account_info)

        if account_info_wrapper.get_subscribers_count() == 0:
            return

        for member in account_info_wrapper.get_members():
            member_wrapper = ViberMemberWrapper(member)
            self.send_text_message(member_wrapper.get_member_id(), message_text)

    def _get_viber_client(self) -> ViberClient:
        access_token = os.environ.get('VIBER_ACCESS_TOKEN')

        if not access_token:
            raise ValueError('VIBER_ACCESS_TOKEN is empty')

        return ViberClient(access_token)
