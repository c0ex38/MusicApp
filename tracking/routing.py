# tracking/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/track_activity/', consumers.TrackActivityConsumer.as_asgi()),
]
