import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .http_response_codes import HTTPResponseCodes
from ..core.prayer_need.prayer_need_service import PrayerNeedService


# Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url,
# containing a JSON-serialized Update
@csrf_exempt
def message(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    update_unicode = request.body.decode('utf-8')
    update = json.loads(update_unicode)

    service = PrayerNeedService()
    service.process_telegram_message(update)
    return HttpResponse(status=HTTPResponseCodes.OK)
