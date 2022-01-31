from django.urls import path, include
from . import views
from .api import telegram_hook_controller as telegram

urlpatterns = [
    path('api/', include('main.api.urls')),
    path('', views.index, name='home')

]
