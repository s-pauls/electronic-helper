from .viber_event_wrapper import ViberEventWrapper
from .viber_service import ViberService
from .viber_user_wrapper import ViberUserWrapper
from ..prayer_need.prayer_need_service import PrayerNeedService


class ViberEventHandler:
    def __init__(self):
        self._viber_service = ViberService()
        self._prayer_need_service = PrayerNeedService()

    def handle(self, viber_event):
        event_name = viber_event['event']

        if event_name == 'webhook':
            return None

        # это событие возникает, когда пользователь первый раз заходит в чат,
        # он еще не подписан, поэтому единственный способ написать ему welcome_message ответить в запросе на это событие
        if event_name == 'conversation_started':

            viber_user_wrapper = ViberUserWrapper(viber_event['user'])
            subscribed = bool(viber_event['subscribed'])

            welcome_message_text = \
                f'Приветствую, {viber_user_wrapper.get_user_name()}!\r\n' \
                f'Я, Электронный помощник церкви \'Благодать\' (Гомель)\r\n' \
                f'Я рассылаю ссылки на YouTube-трансляции.\r\n' \
                f'Также могу передать Вашу молитвенную нужду пастору, просто напишите ее мне\r\n' \
                f'\r\n' \
                f'Чтобы подписаться напишите мне что-нибудь в ответ!'

            welcome_message = {
               'sender': {
                  'name': 'Электронный помощник',
                  # 'avatar': 'http://avatar.example.com'
               },
               # 'tracking_data': 'tracking data',
               'type': 'text',
               'text': welcome_message_text,
               # 'media': 'http://www.images.com/img.jpg',
               # 'thumbnail': 'http://www.images.com/thumb.jpg'
            }

            return welcome_message

        if event_name == 'message':

            viber_event_wrapper = ViberEventWrapper(viber_event)

            if viber_event_wrapper.get_message_type() == 'text':
                self._prayer_need_service.process_message(
                    sender_name=viber_event_wrapper.get_sender_name(),
                    message_id=viber_event_wrapper.get_message_token(),
                    message_text=viber_event_wrapper.get_message_text(),
                    message_source='viber'
                )
            return None

