import json

from django.core.serializers.json import DjangoJSONEncoder


class CustomException(Exception):
    def __init__(self, data):
        if data:
            self.message = 'Custom exception occurred with data:' + json.dumps(data, cls=DjangoJSONEncoder)
        else:
            self.message = 'Custom exception occurred'
