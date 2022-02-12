import json

import requests


# https://www.notion.so/help/add-and-manage-integrations-with-the-api
# Смотри раздел Add integrations to pages для включения интеграции в базе ноушина
from ..utilities.custom_errors import CustomException


class NotionClient:
    def __init__(self, notion_token: str):
        self._token = notion_token

    def send(self, page):
        bearer_token = 'Bearer ' + self._token
        headers = {
            'content-type': 'application/json',
            'Notion-Version': '2021-05-13',
            'Authorization': bearer_token
        }

        response = requests.post('https://api.notion.com/v1/pages/', data=json.dumps(page), headers=headers)

        if response.status_code != 200:
            data = {'response': response.text, 'data': page}
            raise CustomException(data)
