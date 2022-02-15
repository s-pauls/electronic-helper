from .telegram_update_wrapper import TelegramUpdateWrapper
from ..prayer_need.prayer_need_service import PrayerNeedService
from ..ruworship.ruworship_service import RuWorshipService

TELEGRAM_RU_WORSHIP_CHAT_ID = -1001764905737


class TelegramUpdatesHandler:

    def handle(self, telegram_update_object):

        update_wrapper = TelegramUpdateWrapper(telegram_update_object)

        if not update_wrapper.has_message_object():
            return

        chat_id = update_wrapper.get_chat_id()

        if chat_id == TELEGRAM_RU_WORSHIP_CHAT_ID:
            ru_worship_service = RuWorshipService()
            ru_worship_service.process_telegram_message(telegram_update_object)
        else:
            prayer_service = PrayerNeedService()
            prayer_service.process_telegram_message(telegram_update_object)
