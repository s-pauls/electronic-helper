from .push_notification_data_wrapper import PushNotificationDataWrapper
from ..prayer_need.prayer_need_service import PrayerNeedService


class PushNotificationHandler:
    def __init__(self):
        self._prayer_need_service = PrayerNeedService()

    def handle(self, data):
        data_wrapper = PushNotificationDataWrapper(data)

        if data_wrapper.get_app_name() == 'Viber':

            group_name = data_wrapper.get_title()

            if group_name != 'Благодать (Гомель)':
                return

            text = data_wrapper.get_text()

            self._prayer_need_service.process_message(
                sender_name=group_name,
                message_id='-',
                message_text=text,
                message_source='viber'
            )

