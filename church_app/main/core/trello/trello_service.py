import os
from typing import Optional

from trello import TrelloClient, Board, Card

TRELLO_BOARD_YOUTUBE_SERVICE = '6203cd73c8dd867e5a13b868'


class TrelloService:

    def sample(self):
        client = TrelloClient(
            api_key=os.getenv('TRELLO_API_KEY'),
            api_secret=os.getenv('TRELLO_API_SECRET'),
            token=os.getenv('TRELLO_TOKEN'),
            token_secret=os.getenv('TRELLO_TOKEN_SECRET')
        )

        to_do_list_id = '6203cd73c8dd867e5a13b869'
        try:
            self.create_new_preaching_card(
                client=client,
                list_id=to_do_list_id,
                preaching_name='03.012.12 | воскресное служение',  # todo
                preaching_url='https://www.youtube.com/watch?v=hAIE8VOB4pM&list=RDMMhAIE8VOB4pM&start_radio=1'
            )
        except Exception as e:
            print(e)

    def create_new_preaching_card(self, client: TrelloClient, list_id: str, preaching_name: str, preaching_url: str):

        youtube_board = client.get_board(TRELLO_BOARD_YOUTUBE_SERVICE)

        template_card = self.get_first_template_card(youtube_board, 'Template[new_preaching]')

        if template_card is None:
            return

        board_list = youtube_board.get_list(list_id)

        board_list.add_card(
            name=f"Трансляция завершена. Опубликовать проповедь {preaching_name}",
            desc=str.replace(template_card.desc, "{youtube-url}", preaching_url),
            source=template_card.id,
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
