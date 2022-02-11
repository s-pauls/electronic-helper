class YouTubeService:

    # https://cf57722.tmweb.ru/helpers/youtube_auth_response.php
    # https%3A%2F%2Fcf57722.tmweb.ru%2Fhelpers%2Fyoutube_auth_response.php
    # Получения токена: https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id=CLIENT_ID&redirect_uri=https%3A%2F%2Fcf57722.tmweb.ru%2Fhelpers%2Fyoutube_auth_response.php&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=PyYouTube&access_type=offline&prompt=select_account
    # Ответ на запрос https://cf57722.tmweb.ru/helpers/youtube_auth_response.php?code=КОД_ДЛЯ_ТОКЕНА%20https://www.googleapis.com/auth/userinfo.profile%20https://www.googleapis.com/auth/youtube
    # Идем сюда и получаем пару токенов https://cf57722.tmweb.ru/helpers/YouTubeOAuth.html

    def get_active_live_broadcast(self, youtube):
        request = youtube.liveBroadcasts().list(
            part="id,snippet",
            broadcastStatus="active",
            broadcastType="all"
        )
        response = request.execute()
        items = list(response['items'])

        if len(items) > 0:
            return items[0]
        else:
            return None

    def get_live_chat_messages(self, youtube, live_chat_id: str, page_token: str = None):
        request = youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part="id,snippet,authorDetails",
            pageToken=page_token
        )
        response = request.execute()
        return response
