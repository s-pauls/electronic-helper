import os

import pytz as pytz
import json
import datetime

from .notion_client import NotionClient


class NotionService:

    def send_prayer_need(sender_name: str, message_text: str, message_source: str):
        prayers_database_id = 'c4dd9c96b8f94554bb9b020eda4e2667'  # Молитвенные нужды
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        pst_now = utc_now.astimezone(pytz.timezone("Europe/Minsk"))
        data = {
            "parent": {
                "database_id": prayers_database_id
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
                                "content": message_text
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
                        "name": message_source
                    }
                }

            }
        }

        notion_token = os.environ.get('NOTION_TOKEN')

        if notion_token is None:
            raise ValueError('notion_token is empty')

        notion_client = NotionClient(notion_token)
        notion_client.send(json.dumps(data))
