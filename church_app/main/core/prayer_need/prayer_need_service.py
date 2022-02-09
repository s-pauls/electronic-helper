from .prayer_needs_text_analyzer import PrayerNeedsTextAnalyzer
from ..notion.notion_service import NotionService
from ..telegram.telegram_update_wrapper import TelegramUpdateWrapper


class PrayerNeedService:

    def process_telegram_message(self, telegram_update_object):

        update = TelegramUpdateWrapper(telegram_update_object)

        analyzer = PrayerNeedsTextAnalyzer(update.get_message_text())

        if analyzer.is_pray_need():
            notion_service = NotionService()
            sender_name = update.get_first_name() + " " + update.get_last_name()
            notion_service.send_prayer_need(sender_name, update.get_message_text(), 'telegram')
