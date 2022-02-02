from django.http import HttpResponse

from ..core.notion import notion_client


def test(request):
    return HttpResponse("test")