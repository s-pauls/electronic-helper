import json
import logging

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .http_response_codes import HTTPResponseCodes
from ..core.viber.viber_event_handler import ViberEventHandler


@csrf_exempt  # https://www.dev2qa.com/how-to-enable-or-disable-csrf-validation-in-django-web-application/
def viber_event(request):
    if request.method != 'POST':
        return HttpResponse(status=HTTPResponseCodes.FORBIDDEN)

    try:
        event = json.loads(request.body.decode('utf-8'))

        logger = logging.getLogger(__name__)
        logger.info('viber sent event: ' + json.dumps(event, cls=DjangoJSONEncoder))

        handler = ViberEventHandler()
        handler.handle(event)
    except Exception as e:
        logger.exception(e)
        raise

    return HttpResponse(status=HTTPResponseCodes.OK)
