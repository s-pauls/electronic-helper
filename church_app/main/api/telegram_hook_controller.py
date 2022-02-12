import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .http_response_codes import HTTPResponseCodes
from ..core.telegram.telegram_updates_handler import TelegramUpdatesHandler


# Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url,
# containing a JSON-serialized Update
@csrf_exempt  # https://www.dev2qa.com/how-to-enable-or-disable-csrf-validation-in-django-web-application/
def message(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    update_unicode = request.body.decode('utf-8')
    update = json.loads(update_unicode)

    handler = TelegramUpdatesHandler()

    logger = logging.getLogger(__name__)

    try:
        logger.info('telegram sent message: ' + json.dumps(update, cls=DjangoJSONEncoder))
        handler.handle(update)
    except Exception as e:
        logger.exception(e)
        raise

    return HttpResponse(status=HTTPResponseCodes.OK)
