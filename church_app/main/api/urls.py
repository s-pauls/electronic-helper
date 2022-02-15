from django.urls import path
from . import telegram_hook_controller as telegram
from . import viber_hook_controller as viber

urlpatterns = [
    path('telegram/message', telegram.message),
    path('viber/event', viber.viber_event),
]
