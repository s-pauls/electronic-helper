from .prayer_needs_text_analyzer import PrayerNeedsTextAnalyzer
from .remote_bot_default_template_parser import RemoteBotDefaultTemplateParser
from ..notion.notion_service import NotionService
from ..telegram.telegram_update_wrapper import TelegramUpdateWrapper

TELEGRAM_FROM_VIBER_CHAT_ID = -1001681319252
TELEGRAM_FROM_VIBER_CHAT_NAME = 'Благодать (Гомель)'

class PrayerNeedService:

    def process_telegram_message(self, telegram_update_object):

        update = TelegramUpdateWrapper(telegram_update_object)

        if not update.get_message_text():
            return

        message_text = update.get_message_text()
        sender_name = update.get_first_name() + " " + update.get_last_name()

        # в этот чат попадает текст пуш-уведомлений из вайбера
        if update.get_chat_id() == TELEGRAM_FROM_VIBER_CHAT_ID:
            parser = RemoteBotDefaultTemplateParser(message_text)

            if parser.get_caption() != TELEGRAM_FROM_VIBER_CHAT_NAME:
                return

            sender_name = parser.get_sender_name()
            message_text = parser.get_message_text()

        analyzer = PrayerNeedsTextAnalyzer(message_text)

        if analyzer.is_pray_need():
            notion_service = NotionService()

            notion_service.send_prayer_need(sender_name, message_text, 'telegram')
