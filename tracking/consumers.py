import json
from channels.generic.websocket import WebsocketConsumer
from .models import UserActivity, Song
from django.utils import timezone
from asgiref.sync import async_to_sync

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

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
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

        notification = {
            'name': name,
            'store_name': store_name,
            'song_title': song.title if song else 'N/A',
            'message': f"{name} started listening to {song.title if song else 'N/A'} at {store_name}"
        }

        async_to_sync(self.channel_layer.group_send)(
            'admin_notifications',
            {
                'type': 'send_notification',
                'notification': notification
            }
        )

        self.send(text_data=json.dumps(notification))

    def send_notification(self, event):
        notification = event['notification']
        self.send(text_data=json.dumps(notification))

class AdminConsumer(WebsocketConsumer):
    def connect(self):
        async_to_sync(self.channel_layer.group_add)(
            'admin_notifications',
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            'admin_notifications',
            self.channel_name
        )

    def send_notification(self, event):
        notification = event['notification']
        self.send(text_data=json.dumps(notification))
