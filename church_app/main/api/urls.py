from django.urls import path
from . import telegram_hook_controller as telegram

urlpatterns = [
    path('test', telegram.test)
]
