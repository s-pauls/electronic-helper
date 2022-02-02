import pytz as pytz
import json
import requests
import datetime

from .config import NotionConfig


def send(self_data):
    bearer_token = 'Bearer ' + NotionConfig.TOKEN
    headers = {
        'content-type': 'application/json',
        'Notion-Version': '2021-05-13',
        'Authorization': bearer_token
    }

    response = requests.post('https://api.notion.com/v1/pages/', data=self_data, headers=headers)

    if response.text:
        print(response.text)


def send_need(sender_name, text, source):
    utc_now = pytz.utc.localize(datetime.datetime.utcnow())
    pst_now = utc_now.astimezone(pytz.timezone("Europe/Minsk"))
    data = {
        "parent": {
            "database_id": NotionConfig.DATABASE_ID
        },
        "properties": {
            "Дата": {
                "date": {
                    "start": pst_now.isoformat()
                }
            },
            "Нужда": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": text
                        }
                    }
                ]
            },
            "Нуждающийся": {
                "title": [
                    {
                        "text": {
                            "content": sender_name
                        }
                    }
                ]
            },

            "Источник": {
                "select": {
                    "name": source
                }
            }

        }
    }

    send(json.dumps(data))