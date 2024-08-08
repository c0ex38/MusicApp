from django.test import TestCase, Client
from django.urls import reverse
from .models import UserActivity, Song
from django.utils import timezone


class TrackActivityViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.song1 = Song.objects.create(title="Song 1", artist="Artist 1", file="songs/song1.mp3")
        self.song2 = Song.objects.create(title="Song 2", artist="Artist 2", file="songs/song2.mp3")
        self.track_activity_url = reverse('track_activity')

    def test_track_activity_create_new_user_activity(self):
        response = self.client.get(self.track_activity_url, {
            'name': 'Selim SARIKAYA',
            'store_name': 'Store 1',
            'song_id': self.song1.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/templates/tracking/track_activity.html')

        user_activity = UserActivity.objects.get(name='Selim SARIKAYA', store_name='Store 1')
        self.assertEqual(user_activity.song, self.song1.title)
        self.assertEqual(user_activity.name, 'Selim SARIKAYA')
        self.assertEqual(user_activity.store_name, 'Store 1')
        self.assertEqual(user_activity.current_time, '00:00')

    def test_track_activity_update_existing_user_activity(self):
        user_activity = UserActivity.objects.create(
            name='Selim SARIKAYA',
            store_name='Store 1',
            song=self.song1.title,
            last_active=timezone.now(),
            current_time='00:00'
        )

        response = self.client.get(self.track_activity_url, {
            'name': 'Selim SARIKAYA',
            'store_name': 'Store 1',
            'song_id': self.song2.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/templates/tracking/track_activity.html')

        user_activity.refresh_from_db()
        self.assertEqual(user_activity.song, self.song2.title)
        self.assertEqual(user_activity.name, 'Selim SARIKAYA')
        self.assertEqual(user_activity.store_name, 'Store 1')
        self.assertEqual(user_activity.current_time, '00:00')

    def test_track_activity_song_does_not_exist(self):
        response = self.client.get(self.track_activity_url, {
            'name': 'Selim SARIKAYA',
            'store_name': 'Store 1',
            'song_id': 999
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/templates/tracking/track_activity.html')

        user_activity = UserActivity.objects.get(name='Selim SARIKAYA', store_name='Store 1')
        self.assertEqual(user_activity.song, 'Bilinmeyen Şarkı')
        self.assertEqual(user_activity.name, 'Selim SARIKAYA')
        self.assertEqual(user_activity.store_name, 'Store 1')
        self.assertEqual(user_activity.current_time, '00:00')

    def test_track_activity_missing_parameters(self):
        response = self.client.get(self.track_activity_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/templates/tracking/track_activity.html')

        user_activities = UserActivity.objects.all()
        self.assertEqual(user_activities.count(), 0)

    def test_track_activity_template_context(self):
        response = self.client.get(self.track_activity_url, {
            'name': 'Selim SARIKAYA',
            'store_name': 'Store 1',
            'song_id': self.song1.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tracking/templates/tracking/track_activity.html')

        self.assertIn('songs', response.context)
        self.assertIn('announcements', response.context)
        self.assertEqual(list(response.context['songs']), list(Song.objects.all()))
        self.assertEqual(response.context['announcements'], [])
