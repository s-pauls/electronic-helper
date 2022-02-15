from .viber_event_wrapper import ViberEventWrapper
from .viber_service import ViberService
from ..prayer_need.prayer_need_service import PrayerNeedService


class ViberEventHandler:
    def __init__(self):
        self._viber_service = ViberService()
        self._prayer_need_service = PrayerNeedService()

    def handle(self, viber_event):

        viber_event_wrapper = ViberEventWrapper(viber_event)
        event_name = viber_event_wrapper.get_event_name()

        if event_name == 'webhook':
            return

        if event_name == 'conversation_started':

            self._viber_service.send_text_message(
                receiver_id=viber_event_wrapper.get_sender_id(),
                message_text='Приветствую!\r\n'
                             'Я, Электронный помощник церкви \'Благодать\' (Гомель)\r\n'
                             'Я рассылаю ссылки на YouTube-трансляции.\r\n'
                             'Также могу передать Вашу молитвенную нужду пастору, просто напишите ее мне'
            )
            return

        if event_name == 'message':

            if viber_event_wrapper.get_message_type() == 'text':
                self._prayer_need_service.process_message(
                    sender_name=viber_event_wrapper.get_sender_name(),
                    message_id=viber_event_wrapper.get_message_token(),
                    message_text=viber_event_wrapper.get_message_text(),
                    message_source='viber'
                )
            return

