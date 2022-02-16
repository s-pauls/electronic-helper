import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .http_response_codes import HTTPResponseCodes
from ..core.telegram.telegram_updates_handler import TelegramUpdatesHandler
from ..core.viber.viber_event_handler import ViberEventHandler


# Whenever there is an update for the bot, we will send an HTTPS POST request to the specified url,
# containing a JSON-serialized Update


@csrf_exempt  # https://www.dev2qa.com/how-to-enable-or-disable-csrf-validation-in-django-web-application/
def telegram_update(request):
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


@csrf_exempt
def viber_event(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    try:
        event = json.loads(request.body.decode('utf-8'))

        logger = logging.getLogger(__name__)
        logger.info('viber sent event: ' + json.dumps(event, cls=DjangoJSONEncoder))

        handler = ViberEventHandler()
        result = handler.handle(event)

    except Exception as e:
        logger.exception(e)
        raise

    if result is None:
        return HttpResponse(status=HTTPResponseCodes.OK)

    return HttpResponse(
        status=HTTPResponseCodes.OK,
        content=json.dumps(result),
        content_type='application/json'
    )


@csrf_exempt
def android_push_notification(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    push_notification = json.loads(request.body.decode('utf-8'))

    logger = logging.getLogger(__name__)

    try:
        logger.info('telegram sent message: ' + json.dumps(push_notification, cls=DjangoJSONEncoder))
    except Exception as e:
        logger.exception(e)
        raise

    return HttpResponse(status=HTTPResponseCodes.OK)
