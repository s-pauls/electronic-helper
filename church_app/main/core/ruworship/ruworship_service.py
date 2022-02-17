from ..notion.notion_service import NotionService
from ..telegram.telegram_update_wrapper import TelegramUpdateWrapper


class RuWorshipService:

    def process_telegram_message(self, telegram_update_object):

        update = TelegramUpdateWrapper(telegram_update_object)

        if not update.is_message_contain_audio():
            return

        notion_service = NotionService()
        sender_name = update.get_friendly_name()
        notion_service.send_rw_audio_record(sender_name, update.get_audio_filename(), update.get_audio_performer(),  'telegram')
        