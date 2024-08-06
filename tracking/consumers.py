# tracking/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import Song, UserActivity
from django.utils import timezone

class TrackActivityConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        name = data['name']
        store_name = data['store_name']
        song_id = data['song_id']

        if song_id:
            song = Song.objects.get(id=song_id)
        else:
            song = None

        user_activity, created = UserActivity.objects.get_or_create(
            name=name,
            store_name=store_name,
            defaults={'song': song, 'last_active': timezone.now(), 'current_time': '00:00'}
        )

        if not created:
            user_activity.song = song
            user_activity.last_active = timezone.now()
            user_activity.save()

        self.send(text_data=json.dumps({
            'name': name,
            'store_name': store_name,
            'song_title': song.title if song else '',
        }))
