from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/activity/$', consumers.ActivityConsumer.as_asgi()),
    re_path(r'ws/admin/$', consumers.AdminConsumer.as_asgi()),
]
