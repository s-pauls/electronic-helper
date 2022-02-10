import requests

from ...utilities.custom_errors import CustomException


class VkClient:

    # https://dev.vk.com/method/wall.post
    def wall_post(self, access_token: str, owner_id: int, message: str, attachments: str):

        data = {
            'access_token': access_token,
            'owner_id': owner_id,
            'from_group': 1, # 1 — запись будет опубликована от имени группы, 0 — запись будет опубликована от имени пользователя (по умолчанию).
            'message': message,
            'signed': 0,
            'v': "5.131",
            'attachments': attachments
        }

        response = requests.post('https://api.vk.com/method/wall.post', data)

        if response.status_code != 200:
            data = {'response': response.text, 'data': data}
            raise CustomException(data)

    def get_audio_ids(self, session: requests.Session, owner_id: int, offset: int, album_id=None, access_hash=None):
        data = {
            'act': 'load_section',
            'owner_id': owner_id,
            'playlist_id': album_id if album_id else -1,
            'offset': offset,
            'type': 'playlist',
            'access_hash': access_hash,
            'is_loading_all': 1
        }

        response = session.http.post(
            'https://m.vk.com/audio',
            data=data,
            allow_redirects=False
        ).json()

        if not response['data'][0]:
            raise Exception(
                'You don\'t have permissions to browse {}\'s albums'.format(
                    owner_id
                )
            )

        ids = scrap_ids(
            response['data'][0]['list']
        )

        return ids


def scrap_ids(audio_data):
    """ Парсинг списка хэшей аудиозаписей из json объекта """
    ids = []

    for track in audio_data:
        id_str = str(track[0])
        if id_str:
            ids.append(int(id_str))

    return ids