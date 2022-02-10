import os
import random
import vk_api
import logging


from .job_base import JobBase
from ..core.vk.vk_client import VkClient


class RuWorshipTheeSongs(JobBase):
    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())

    def execute(self, parameters):

        access_token = os.environ.get('VK_RU_WORSHIP_TOKEN')
        login = os.environ.get('VK_GOMEL_GRACE_LOGIN')
        password = os.environ.get('VK_GOMEL_GRACE_PASSWORD')
        group_id_for_posting = -57836995
        group_id_for_retrieving_songs = -53248741

        logger = logging.getLogger(__name__)
        vk_session = vk_api.VkApi(login, password)

        try:
            vk_session.auth()
        except vk_api.AuthError as error_msg:
            logger.error(error_msg)
            return

        # Этот метод выгребает все 4804+ записи!!!
        # Требуется оптимизация
        # vk_audio = VkAudio(vk_session)
        # tracks = vk_audio.get(owner_id=group_id_for_retrieving_songs)  # 4804 песен

        # не получилось воспользоваться методом библиотеки vk_api
        # - для публикации поста (не сработал )
        # - слишком долго собирает информацию о треке, хотя нам нужен только id
        # пришлось сделать свой клиент
        vk_client = VkClient()
        ids = vk_client.get_audio_ids(vk_session,
                                      owner_id=group_id_for_retrieving_songs,
                                      offset=random.randint(1, 4800))

        # перемешиваю
        random.shuffle(ids)

        attachments: str = ''
        for id in ids[:3]:
            attachments = attachments + (
                '' if not attachments else ',') + f"audio{group_id_for_retrieving_songs}_{id}"

        attachments = attachments + ('' if not attachments else ',') + 'photo-53248741_457253603'

        vk_client.wall_post(access_token=access_token,
                            owner_id=group_id_for_posting,
                            message='Прославляй Господа вместе с RuWorship!\r\n\r\n#Прославлениенарусском #Хвала #RuWorship',
                            attachments=attachments)