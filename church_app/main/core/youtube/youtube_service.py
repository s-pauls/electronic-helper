from datetime import datetime
from ..utilities import datetime_helper
from ...models import YouTubeBroadcastsDb


class YouTubeService:

    # https://cf57722.tmweb.ru/helpers/youtube_auth_response.php
    # https%3A%2F%2Fcf57722.tmweb.ru%2Fhelpers%2Fyoutube_auth_response.php
    # Получения токена: https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=CLIENT_ID&redirect_uri=https%3A%2F%2Fcf57722.tmweb.ru%2Fhelpers%2Fyoutube_auth_response.php&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=PyYouTube&access_type=offline&prompt=select_account
    # Ответ на запрос https://cf57722.tmweb.ru/helpers/youtube_auth_response.php?code=КОД_ДЛЯ_ТОКЕНА%20https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/youtube
    # Идем сюда и получаем пару токенов https://cf57722.tmweb.ru/helpers/YouTubeOAuth.html

    def get_active_live_broadcast(self, youtube, part='id,snippet'):
        request = youtube.liveBroadcasts().list(
            part=part,
            broadcastStatus="active",
            broadcastType="all"
        )
        response = request.execute()
        items = list(response['items'])

        if len(items) > 0:
            return items[0]
        else:
            return None

    def get_live_broadcast_by_id(self, youtube, youtube_id: str, part: str = 'snippet,status'):
        request = youtube.liveBroadcasts().list(
            part=part,
            id=youtube_id
        )
        response = request.execute()
        items = list(response['items'])

        if len(items) > 0:
            return items[0]
        else:
            return None

    # Возвращает список запланированных трансляций от ближайшей 5 шт. (по умолчанию)
    def get_upcoming_live_broadcast(self, youtube, part: str = 'id,snippet,status'):
        request = youtube.liveBroadcasts().list(
            part=part,
            maxResults=50,
            broadcastStatus="upcoming",
            broadcastType="event"
        )
        response = request.execute()
        items = list(response['items'])
        return items

    def get_live_chat_messages(self, youtube, live_chat_id: str, page_token: str = None):
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="id,snippet,authorDetails",
            pageToken=page_token
        )
        response = request.execute()
        return response

    def insert_live_chat_message(self, youtube, live_chat_id: str, message_text: str):
        request = youtube.liveChatMessages().insert(
            part="snippet",
            body={
                "snippet": {
                    "liveChatId": live_chat_id,
                    "type": "textMessageEvent",
                    "textMessageDetails": {
                        "messageText": message_text
                    }
                }
            }
        )
        response = request.execute()

    def add_new_live_broadcast_in_db(self, youtube_id: str, youtube_title: str,
                                live_chat_id: str,
                                scheduled_start_time : datetime,
                                broadcast_status: str = 'active'):
        row = YouTubeBroadcastsDb(
            youtube_id=youtube_id,
            youtube_title=youtube_title,
            status=broadcast_status,
            live_chat_id=live_chat_id,
            create_datetime=datetime_helper.now_with_utc_timezone(),
            scheduled_start_time=datetime_helper.add_utc_time_zone(scheduled_start_time)
        )

        row.save()

    def get_active_live_broadcast_from_db(self) -> YouTubeBroadcastsDb:
        rows = list(YouTubeBroadcastsDb.objects.filter(status='active').order_by('-create_datetime'))
        if len(rows) > 0:
            return rows[0]
        else:
            return None

    def get_live_broadcast_by_youtube_id_from_db(self, youtube_id: str) -> YouTubeBroadcastsDb:
        return YouTubeBroadcastsDb.objects.get(youtube_id=youtube_id)


    def set_live_broadcast_finished(self, youtube_id: str):
        row = YouTubeBroadcastsDb.objects.get(youtube_id=youtube_id)
        row.status = 'finished'
        row.save()

    def set_live_broadcast_page_token(self, youtube_id: str, page_token: str):
        row = YouTubeBroadcastsDb.objects.get(youtube_id=youtube_id)
        row.live_chat_next_page_token = page_token
        row.save()
