import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .http_response_codes import HTTPResponseCodes
from ..core.push_notification.push_notification_handler import PushNotificationHandler
from ..core.telegram.telegram_updates_handler import TelegramUpdatesHandler
from ..core.viber.viber_event_handler import ViberEventHandler
from ..core.vk.vk_callback_handler import VkCallbackHandler


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

    logger = logging.getLogger(__name__)

    try:
        data = {
            'name': request.POST.get('name'),
            'pkg': request.POST.get('pkg'),
            'title': request.POST.get('title'),
            'text': request.POST.get('text'),
            'subtext': request.POST.get('subtext'),
            'bigtext': request.POST.get('bigtext'),
            'infotext': request.POST.get('infotext'),
            'user': request.POST.get('user'),
        }

        logger.info('notification forward sent message: ' + json.dumps(data, cls=DjangoJSONEncoder))

        handler = PushNotificationHandler()
        handler.handle(data)

    except Exception as e:
        logger.exception(e)
        raise

    return HttpResponse(status=HTTPResponseCodes.OK)


@csrf_exempt
def vk_callback(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    logger = logging.getLogger(__name__)

    try:
        data = json.loads(request.body.decode('utf-8'))

        logger.info('vk sent message: ' + json.dumps(data, cls=DjangoJSONEncoder))

        handler = VkCallbackHandler()
        result = handler.handle(data)

    except Exception as e:
        logger.exception(e)
        raise

    print(result)

    if result is None:
        return HttpResponse(status=HTTPResponseCodes.OK)

    object_type = result.get('type')

    if object_type and object_type == 'confirmation':
        return HttpResponse(
            status=HTTPResponseCodes.OK,
            content=result.get('answer')

        )

    return HttpResponse(
        status=HTTPResponseCodes.OK,
        content=json.dumps(result),
        content_type='application/json'
    )