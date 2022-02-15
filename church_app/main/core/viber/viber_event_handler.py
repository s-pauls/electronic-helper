from .viber_event_wrapper import ViberEventWrapper
from ..prayer_need.prayer_need_service import PrayerNeedService


class ViberEventHandler:

    def handle(self, viber_event):

        viber_event_wrapper = ViberEventWrapper(viber_event)
        event_name = viber_event_wrapper.get_event_name()

        if event_name == 'webhook':
            return

        if event_name == 'message':
            return

