# tracking/tests.py
from django.test import TestCase, Client
from channels.testing import WebsocketCommunicator
from django.urls import reverse
from .models import Song, UserActivity
from .consumers import TrackActivityConsumer
import json

class HomeViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_redirect(self):
        response = self.client.get(reverse('home'), {'name': 'Selim', 'store': 'Aykent'})
        self.assertRedirects(response, '/track/?name=Selim&store=Aykent')


class TrackActivityViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.song = Song.objects.create(title='Test Song', artist='Test Artist')

    def test_track_activity_get(self):
        response = self.client.get(reverse('track_activity'), {'name': 'Selim', 'store': 'Aykent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Selim')
        self.assertContains(response, 'Aykent')

    def test_track_activity_post(self):
        response = self.client.get(reverse('track_activity'), {'name': 'Selim', 'store': 'Aykent', 'song_id': self.song.id})
        self.assertEqual(response.status_code, 200)
        user_activity = UserActivity.objects.get(name='Selim', store_name='Aykent')
        self.assertEqual(user_activity.song, self.song)


class TrackActivityConsumerTest(TestCase):
    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(TrackActivityConsumer.as_asgi(), "/ws/track_activity/")
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        # Send message from WebSocket
        await communicator.send_json_to({
            'name': 'Selim',
            'store_name': 'Aykent',
            'song_id': None
        })

        # Receive message from WebSocket
        response = await communicator.receive_json_from()
        self.assertEqual(response['name'], 'Selim')
        self.assertEqual(response['store_name'], 'Aykent')
        self.assertEqual(response['song_title'], '')

        await communicator.disconnect()


class AdminActivityViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_admin_activity_page(self):
        response = self.client.get(reverse('admin_activity'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Activities')
