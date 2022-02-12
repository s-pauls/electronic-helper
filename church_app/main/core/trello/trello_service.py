import pytz
from datetime import datetime, timedelta
from typing import Optional
from trello import Board, Card
from .trello_composer import TrelloComposer

TRELLO_BOARD_YOUTUBE_SERVICE = '6203cd73c8dd867e5a13b868'


class TrelloService:

    def create_new_preaching_card(self, youtube_title: str, youtube_url: str):

        client = TrelloComposer().compose()

        youtube_board = client.get_board(TRELLO_BOARD_YOUTUBE_SERVICE)

        template_card = self.get_first_template_card(youtube_board, 'Template[new_preaching]')

        if template_card is None:
            return

        to_do_list_id = '6203cd73c8dd867e5a13b869'
        board_list = youtube_board.get_list(to_do_list_id)

        board_list.add_card(
            name=f"Опубликовать проповедь. Трансляция {youtube_title}",
            desc=str.replace(template_card.desc, "{youtube-url}", youtube_url),
            source=template_card.id,
            position='top'
        )

    def create_update_youtube_description_card(self, youtube_title: str, youtube_url: str):

        client = TrelloComposer().compose()

        youtube_board = client.get_board(TRELLO_BOARD_YOUTUBE_SERVICE)

        template_card = self.get_first_template_card(youtube_board, 'Template[update_broadcast_description]')

        if template_card is None:
            return

        to_do_list_id = '6203cd73c8dd867e5a13b869'
        board_list = youtube_board.get_list(to_do_list_id)

        tz = pytz.timezone('Europe/Minsk')
        today = datetime.now(tz=tz)
        start_of_day = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(1)

        board_list.add_card(
            name=f"Обновить тайм-коды. Трансляция {youtube_title}",
            desc=str.replace(template_card.desc, "{youtube-url}", youtube_url),
            source=template_card.id,
            due=end_of_day.isoformat(),
            position='top'
        )

    def get_template_cards(self, board: Board, template_name_start: str = 'Template') -> [Card]:
        cards = board.get_cards(card_filter='open')
        template_cards = (card for card in cards if card.name.startswith(template_name_start))
        return list(template_cards)

    def get_first_template_card(self, board: Board, template_name_start: str) -> Optional[Card]:
        cards = self.get_template_cards(board, template_name_start)
        if len(cards) == 0:
            return None

        if len(cards) > 1:
            raise ValueError('too match cards')

        return cards[0]
