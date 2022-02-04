from .prayer_needs_text_analyzer import PrayerNeedsTextAnalyzer
from ..notion.notion_service import NotionService
from ..telegram.telegram_message import TelegramMessage


class PrayerNeedService:

    def process_telegram_message(self, telegram_update_object):

        message = TelegramMessage(telegram_update_object)
        analyzer = PrayerNeedsTextAnalyzer(message.get_text())

        if analyzer.is_pray_need():
            notion_service = NotionService
            sender_name = message.get_first_name() + " " + message.get_last_name()
            notion_service.send_prayer_need(sender_name, message.get_text(), 'telegram')
