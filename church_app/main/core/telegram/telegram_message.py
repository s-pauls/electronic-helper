# Constant for type Inline Query.
INLINE_QUERY = 'inline_query'

# Constant for type Callback Query.
CALLBACK_QUERY = 'callback_query'

# Constant for type Edited Message.
EDITED_MESSAGE = 'edited_message'

# Constant for type Reply.
REPLY = 'reply'

# Constant for type Message.
MESSAGE = 'message'

# Constant for type Photo.
PHOTO = 'photo'

# Constant for type Video.
VIDEO = 'video'

# Constant for type Audio.
AUDIO = 'audio'

# Constant for type Voice.
VOICE = 'voice'

# Constant for type animation.
ANIMATION = 'animation'

# Constant for type sticker.
STICKER = 'sticker'

# Constant for type Document.
DOCUMENT = 'document'

# Constant for type Location.
LOCATION = 'location'

# Constant for type Contact.
CONTACT = 'contact'

# Constant for type Channel Post.
CHANNEL_POST = 'channel_post'


class TelegramMessage:
    def __init__(self, body):
        self._BODY = body

    def get_text(self) -> str:

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['data']

        if _type == CHANNEL_POST:
            return self._BODY['channel_post']['text']

        if _type == EDITED_MESSAGE:
            return self._BODY['edited_message']['text']

        return self._BODY['message']['text']

    def get_first_name(self) -> str:

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['from']['first_name']

        if _type == CHANNEL_POST:
            return self._BODY['channel_post']['from']['first_name']

        if _type == EDITED_MESSAGE:
            return self._BODY['edited_message']['from']['first_name']

        return self._BODY['message']['from']['first_name']

    def get_last_name(self) -> str:

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['from']['last_name']

        if _type == CHANNEL_POST:
            return self._BODY['channel_post']['from']['last_name']

        if _type == EDITED_MESSAGE:
            return self._BODY['edited_message']['from']['last_name']

        if _type == MESSAGE:
            return self._BODY['message']['from']['last_name']

        return ''

    def get_user_id(self) -> int:

        _type = self._get_type()
        _result: str

        if _type == CALLBACK_QUERY:
            return int(self._BODY['callback_query']['from']['id'])

        if _type == CHANNEL_POST:
            return int(self._BODY['channel_post']['from']['id'])

        if _type == EDITED_MESSAGE:
            return int(self._BODY['edited_message']['from']['id'])

        return int(self._BODY['message']['from']['id'])

    def get_chat_id(self):

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return int(self._BODY['callback_query']['message']['chat']['id'])

        if _type == CHANNEL_POST:
            return int(self._BODY['channel_post']['chat']['id'])

        if _type == EDITED_MESSAGE:
            return int(self._BODY['edited_message']['chat']['id'])

        if _type == INLINE_QUERY:
            return int(self._BODY['inline_query']['from']['id'])

        return int(self._BODY['message']['chat']['id'])

    def message_from_group(self) -> bool:
        if self._BODY['message']['chat']['type'] == 'private':
            return False
        return True

    def get_user_name(self) -> str:

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['from']['username']

        if _type == CHANNEL_POST:
            return self._BODY['channel_post']['from']['username']

        if _type == EDITED_MESSAGE:
            return self._BODY['edited_message']['from']['username']

        return self._BODY['message']['from']['username']

    def get_location(self) -> str:
        return self._BODY['message']['location']

    def _get_type(self):

        if self._BODY.get('inline_query') is not None:
            return INLINE_QUERY

        if self._BODY.get('callback_query') is not None:
            return CALLBACK_QUERY

        if self._BODY.get('edited_message') is not None:
            return EDITED_MESSAGE

        if self._BODY.get('message', {}).get('text') is not None:
            return MESSAGE

        if self._BODY.get('message', {}).get('photo') is not None:
            return PHOTO

        if self._BODY.get('message', {}).get('video') is not None:
            return VIDEO

        if self._BODY.get('message', {}).get('audio') is not None:
            return AUDIO

        if self._BODY.get('message', {}).get('voice') is not None:
            return VOICE

        if self._BODY.get('message', {}).get('contact') is not None:
            return CONTACT

        if self._BODY.get('message', {}).get('location') is not None:
            return LOCATION

        if self._BODY.get('message', {}).get('reply_to_message') is not None:
            return REPLY

        if self._BODY.get('message', {}).get('animation') is not None:
            return ANIMATION

        if self._BODY.get('message', {}).get('sticker') is not None:
            return STICKER

        if self._BODY.get('message', {}).get('document') is not None:
            return DOCUMENT

        if self._BODY.get('channel_post') is not None:
            return CHANNEL_POST

        return None
