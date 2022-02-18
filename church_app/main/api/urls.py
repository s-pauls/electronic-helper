from django.urls import path
from . import web_hook_controller as controller


urlpatterns = [
    path('telegram/message', controller.telegram_update),
    path('viber/event', controller.viber_event),
    path('notification_forward/push_notification', controller.android_push_notification),
    path('vk/callback', controller.vk_callback),
]
