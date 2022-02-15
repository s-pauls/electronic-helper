import json
import requests

from ..utilities.custom_errors import CustomException


# https://developers.viber.com/docs/api/rest-bot-api/
class ViberClient:
    def __init__(self, viber_token: str):
        self._token = viber_token

    # возвращает сведенья о боте и список подписчиков
    def get_account_info(self):
        headers = {
            'X-Viber-Auth-Token': self._token
        }

        data = {}

        response = requests.post('https://chatapi.viber.com/pa/get_account_info',
                                 data=json.dumps(data),
                                 headers=headers)

        if response.status_code != 200:
            data = {'response': response.text}
            raise CustomException(data)

        return json.loads(response.text)

    # receiver_id - subscribed valid user id
    def send_text_message(self, receiver_id: str, message_text: str):
        headers = {
            'X-Viber-Auth-Token': self._token
        }

        data = {
           'receiver': receiver_id,
           'min_api_version': 1,
           'sender': {
              'name': 'Электронный помощник',
              # 'avatar': 'http://avatar.example.com'
           },
           # 'tracking_data': 'tracking data',
           'type': 'text',
           'text': message_text
        }

        response = requests.post('https://chatapi.viber.com/pa/send_message',
                                 data=json.dumps(data),
                                 headers=headers)

        if response.status_code != 200:
            data = {'response': response.text, 'data': data}
            raise CustomException(data)

        return json.loads(response.text)
