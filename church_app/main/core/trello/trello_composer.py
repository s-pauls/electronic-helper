import os

from trello import TrelloClient


class TrelloComposer:

    def compose(self) -> TrelloClient:
        client = TrelloClient(
            api_key=os.getenv('TRELLO_API_KEY'),
            api_secret=os.getenv('TRELLO_API_SECRET'),
            token=os.getenv('TRELLO_TOKEN'),
            token_secret=os.getenv('TRELLO_TOKEN_SECRET')
        )

        return client