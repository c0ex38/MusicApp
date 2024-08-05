# tracking/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer
from .models import UserActivity

class ActivityConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        name = data['name']
        store_name = data['store_name']
        song_id = data['song_id']
        timestamp = data['timestamp']

        activity = UserActivity.objects.get(name=name, store_name=store_name)
        activity.song_id = song_id
        activity.last_active = timestamp
        activity.save()

        self.send(text_data=json.dumps({
            'name': name,
            'store_name': store_name,
            'song': activity.song.title if activity.song else '',
            'timestamp': timestamp
        }))


