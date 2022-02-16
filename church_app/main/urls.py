from django.urls import path, include
from . import views

urlpatterns = [
    path('api/', include('main.api.urls')),
    path('', views.index, name='home')

]
