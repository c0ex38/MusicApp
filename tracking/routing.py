# tracking/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/activity/', consumers.ActivityConsumer.as_asgi()),
]
