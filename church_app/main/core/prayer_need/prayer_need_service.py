from .prayer_needs_text_analyzer import PrayerNeedsTextAnalyzer
from ..notion.notion_service import NotionService
from ..telegram.telegram_update import TelegramUpdate


class PrayerNeedService:

    def process_telegram_message(self, telegram_update_object):

        update = TelegramUpdate(telegram_update_object)

        if not update.is_message_object():
            return

        if update.get_message_text() is None:
            return

        analyzer = PrayerNeedsTextAnalyzer(update.get_text())

        if analyzer.is_pray_need():
            notion_service = NotionService
            sender_name = update.get_first_name() + " " + update.get_last_name()
            notion_service.send_prayer_need(sender_name, update.get_text(), 'telegram')
