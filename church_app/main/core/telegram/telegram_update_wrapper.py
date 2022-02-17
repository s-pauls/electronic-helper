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

EDITED_CHANNEL_POST = 'edited_channel_post'


# https://core.telegram.org/bots/api#update
class TelegramUpdateWrapper:
    def __init__(self, body):
        self._BODY = body

    def get_message_id(self) -> int:

        if self.has_message_object():
            message = self.get_message_object()
            return int(message.get('message_id'))

        raise ValueError()

    def get_message_text(self) -> str:

        if self.has_message_object():
            message = self.get_message_object()
            return message.get('text')

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['data']

        return ''

    def get_message_caption(self) -> str:
        message = self.get_message_object()
        return message.get('caption', '')

    def get_first_name(self) -> str:

        if self.has_message_object():
            sender = self._get_message_sender()
            if sender is None:
                return ''

            return sender['first_name']

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['from']['first_name']

        return ''

    def get_last_name(self) -> str:

        if self.has_message_object():
            sender = self._get_message_sender()
            if sender is None:
                return ''

            return sender.get('last_name', '')

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['from']['last_name']

        return ''

    def get_user_name(self) -> str:

        if self.has_message_object():
            sender = self._get_message_sender()
            if sender is None:
                return ''

            return sender.get('username', '')

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return self._BODY['callback_query']['from']['username']

    def get_user_id(self) -> int:

        if self.has_message_object():
            sender = self._get_message_sender()
            if sender is None:
                raise ValueError()

            return int(sender['id'])

        _type = self._get_type()

        if _type == CALLBACK_QUERY:
            return int(self._BODY['callback_query']['from']['id'])

        raise ValueError()

    def get_chat_id(self) -> int:

        if self.has_message_object():
            chat = self._get_message_chat()
            return int(chat['id'])

        _type = self._get_type()

        if _type == INLINE_QUERY:
            return int(self._BODY['inline_query']['from']['id'])

        if _type == CALLBACK_QUERY:
            return int(self._BODY['callback_query']['message']['chat']['id'])

        raise ValueError()

    def message_from_group(self) -> bool:
        if self._BODY['message']['chat']['type'] == 'private':
            return False
        return True

    def is_message_contain_audio(self) -> bool:
        _type = self._get_type()
        return _type == AUDIO

    # Optional. Original filename as defined by sender
    def get_audio_filename(self) -> str:
        message = self.get_message_object()
        return message['audio'].get('file_name', '')

    # Optional. MIME type of the file as defined by sender
    def get_audio_mimetype(self) -> str:
        message = self.get_message_object()
        return message['audio'].get('mime_type', '')

    # Optional. Performer of the audio as defined by sender or by audio tags
    def get_audio_performer(self) -> str:
        message = self.get_message_object()
        return message['audio'].get('performer', '')

    def has_message_object(self) -> bool:
        if self._BODY.get('message') is not None:
            return True

        if self._BODY.get('edited_message') is not None:
            return True

        if self._BODY.get('channel_post') is not None:
            return True

        if self._BODY.get('edited_channel_post') is not None:
            return True

        return False

    def get_message_object(self):
        return self._BODY.get('message',
                              self._BODY.get('edited_message',
                                             self._BODY.get('channel_post',
                                                            self._BODY.get('edited_channel_post'))))

    def _get_message_sender(self):
        # Sender of the message; empty for messages sent to channels.
        message = self.get_message_object()
        if 'from' in message:
            return message.get('from')
        else:
            return None

    def _get_message_chat(self):
        # Sender of the message; empty for messages sent to channels.
        message = self.get_message_object()
        return message['chat']

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

        if self._BODY.get('edited_channel_post') is not None:
            return EDITED_CHANNEL_POST

        return None
