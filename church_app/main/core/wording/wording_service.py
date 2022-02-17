from datetime import datetime
from ..utilities import datetime_helper


class WordingService:
    def __init__(self):
        pass

    def get_youtube_live_broadcast_wording(self, youtube_id: str, title: str, scheduled_start_time: datetime):

        if datetime_helper.is_sunday(scheduled_start_time):
            message_text = 'Наступил этот день воскресенья!\r\n' \
                           'Предавай все дела забвенью!\r\n' \
                           'Подключись, чтобы услышать слово!\r\n' \
                           '\r\n' \
                           'Трансляция в {TIME}:\r\n' \
                           'https://youtu.be/{YOUTUBE_ID}'
        # todo Добавить формулировки для рождественского и пасхального служений
        # if 'Рождеств' in title:
        else:
            message_text = 'Трансляция в {TIME}:\r\n' \
                           'https://youtu.be/{YOUTUBE_ID}'

        dt = datetime_helper.add_minsk_time_zone(scheduled_start_time)

        message_text = message_text\
            .replace('{YOUTUBE_ID}', youtube_id)\
            .replace('{TIME}', dt.strftime('%H:%M'))

        return message_text
