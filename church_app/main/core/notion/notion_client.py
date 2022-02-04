import requests


class NotionClient:
    def __init__(self, notion_token: str):
        self._token = notion_token

    def send(self, self_data):
        bearer_token = 'Bearer ' + self._token
        headers = {
            'content-type': 'application/json',
            'Notion-Version': '2021-05-13',
            'Authorization': bearer_token
        }

        response = requests.post('https://api.notion.com/v1/pages/', data=self_data, headers=headers)