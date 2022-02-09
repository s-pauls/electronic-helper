import datetime
import os


from .notion_client import NotionClient
from .notion_page_builder import NotionPageBuilder


class NotionService:

    def send_prayer_need(self, sender_name: str, message_text: str, message_source: str):

        notion_token = os.environ.get('NOTION_TOKEN')

        if not notion_token:
            raise ValueError('NOTION_TOKEN is empty')

        database_id = 'c4dd9c96b8f94554bb9b020eda4e2667'  # Молитвенные нужды

        page_builder = NotionPageBuilder(database_id)
        page_builder.add_date('Дата', datetime.datetime.utcnow())
        page_builder.add_text('Нужда', message_text)
        page_builder.add_title('Нуждающийся', sender_name)
        page_builder.add_select('Источник', message_source)

        page = page_builder.page

        notion_client = NotionClient(notion_token)
        notion_client.send(page)

    def send_rw_audio_record(self, sender_name: str, file_name: str, performer: str, message_source: str):

        notion_token = os.environ.get('NOTION_RU_WORSHIP_TOKEN')

        if not notion_token:
            raise ValueError('NOTION_RU_WORSHIP_TOKEN is empty')

        # база с записями песен, которые нужно валидировать для ruworship
        database_id = '46a159b340204e8b9dfc2673d5bf2ab9'

        page_builder = NotionPageBuilder(database_id)
        page_builder.add_title('Название трека', file_name)
        page_builder.add_text('Исполнитель', performer)
        page_builder.add_select('Источник', message_source)
        page_builder.add_text('Отправитель', sender_name)
        page_builder.add_select('Статус обработки', 'необработан')

        page = page_builder.page

        notion_client = NotionClient(notion_token)
        notion_client.send(page)
