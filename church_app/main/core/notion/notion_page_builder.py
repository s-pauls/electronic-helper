import datetime
import pytz as pytz


class NotionPageBuilder:
    def __init__(self, database_id: str) -> None:
        self._page: dict = None
        self.reset(database_id)

    def reset(self, database_id: str) -> None:
        self._page = {
            'parent': {
                'database_id': database_id
            },
            'properties': {}
        }

    @property
    def page(self):
        page = self._page
        self.reset('')
        return page

    def add_title(self, name: str, value: str) -> None:
        title_object = {name: {'title': [{'text': {'content': value}}]}}
        properties = self._page.get('properties')
        properties.update(title_object)

    def add_date(self, name: str, value: datetime) -> None:
        utc_now = pytz.utc.localize(value)
        pst_now = utc_now.astimezone(pytz.timezone('Europe/Minsk'))
        date_object = {name: {'date': {'start': pst_now.isoformat()}}}
        properties = self._page.get('properties')
        properties.update(date_object)

    def add_text(self, name: str, value: str) -> None:
        rich_text_object = {name: {'rich_text': [{'type': 'text', 'text': {'content': value}}]}}
        properties = self._page.get('properties')
        properties.update(rich_text_object)

    def add_select(self, name: str, value: str) -> None:
        select_object = {name: {'select': {'name': value}}}
        properties = self._page.get('properties')
        properties.update(select_object)
