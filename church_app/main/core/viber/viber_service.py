import os


from .viber_client import ViberClient
from ...models import SubscriberDb


class ViberService:

    def send_text_message(self, receiver_id: str, message_text: str):
        viber_client = self._get_viber_client()
        viber_client.send_text_message(receiver_id, message_text)

    def send_text_message_to_all_subscribers(self, message_text: str):
        subscribers = self.get_subscribers_from_db()

        if len(subscribers) > 0:
            for subscriber in subscribers:
                self.send_text_message(subscriber.user_id, message_text)

    def save_subscriber_into_db(self, user_id: str, user_name: str, user_avatar: str, user_language: str):

        # https://docs.djangoproject.com/en/1.8/ref/models/querysets/#update
        updated_rows_count = SubscriberDb.objects\
            .filter(user_id=user_id)\
            .update(user_name=user_name,
                    user_avatar=user_avatar,
                    user_language=user_language
                    )

        if updated_rows_count == 0:
            row = SubscriberDb(
                user_id=user_id,
                user_name=user_name,
                user_avatar=user_avatar,
                user_language=user_language,
                subscribed_to='viber-gomelgrace-bot'
            )
            row.save()

    def set_subscribed_status(self, user_id: str):
        SubscriberDb.objects\
            .filter(user_id=user_id)\
            .update(subscription_status='subscribed')

    def set_unsubscribed_status(self, user_id: str):
        SubscriberDb.objects \
            .filter(user_id=user_id) \
            .update(subscription_status='unsubscribed')

    def get_subscribers_from_db(self) -> [SubscriberDb]:
        rows = SubscriberDb.objects.filter(subscribed_to='viber-gomelgrace-bot', subscription_status='subscribed')
        return list(rows)

    def _get_viber_client(self) -> ViberClient:
        access_token = os.environ.get('VIBER_ACCESS_TOKEN')

        if not access_token:
            raise ValueError('VIBER_ACCESS_TOKEN is empty')

        return ViberClient(access_token)