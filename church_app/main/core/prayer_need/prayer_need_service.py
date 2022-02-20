import logging

from .prayer_needs_text_analyzer import PrayerNeedsTextAnalyzer
from .remote_bot_default_template_parser import RemoteBotDefaultTemplateParser
from ..notion.notion_service import NotionService
from ..telegram.telegram_update_wrapper import TelegramUpdateWrapper

TELEGRAM_FROM_VIBER_CHAT_ID = -1001681319252
TELEGRAM_FROM_VIBER_CHAT_NAME = 'Благодать (Гомель)'


class PrayerNeedService:

    def __init__(self):
        self._notion_service = NotionService()
        self._logger = logging.getLogger(__name__)

    def process_telegram_message(self, telegram_update_object):

        update = TelegramUpdateWrapper(telegram_update_object)

        if not update.get_message_text():
            return

        message_id = update.get_message_id()
        message_text = update.get_message_text()
        sender_name = update.get_friendly_name()

        if update.get_chat_id() == TELEGRAM_FROM_VIBER_CHAT_ID:
            self._logger.debug(f'Message id: {message_id}. '
                               f'Processing message from Telegram\'s Viber retranslator')
            # в этот чат попадает текст всех пуш-уведомлений из всех групп Вайбера
            parser = RemoteBotDefaultTemplateParser(message_text)

            if parser.get_caption() != TELEGRAM_FROM_VIBER_CHAT_NAME:
                self._logger.debug(f'Message id: {message_id}. '
                                   f'Processing interrupted due to this viber group was not expected')
                return

            sender_name = parser.get_sender_name()
            message_text = parser.get_message_text()

            self.process_message(sender_name, str(message_id), message_text, 'viber')

        else:
            self.process_message(sender_name, str(message_id), message_text, 'telegram')

    def process_message(self, sender_name: str, message_id: str, message_text: str, message_source: str) -> bool:

        analyzer = PrayerNeedsTextAnalyzer(message_text)

        if analyzer.is_pray_need():
            self._notion_service.send_prayer_need(sender_name, message_text, message_source)

            return True

        self._logger.debug(f'Message id: {message_id}. '
                           f'Processing interrupted due to message has not prayers need')
        return False
