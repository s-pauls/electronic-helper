import json
import logging

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .http_response_codes import HTTPResponseCodes
from ..core.prayer_need.prayer_need_service import PrayerNeedService


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url,
# containing a JSON-serialized Update
@csrf_exempt
def message(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    update_unicode = request.body.decode('utf-8')
    update = json.loads(update_unicode)

    service = PrayerNeedService()

    try:
        logger.info('telegram sent message: ' + json.dumps(update))
        service.process_telegram_message(update)
    except Exception as e:
        logger.error(e)
        raise

    return HttpResponse(status=HTTPResponseCodes.OK)
