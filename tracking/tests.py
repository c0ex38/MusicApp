from django.test import TestCase, Client
from django.urls import reverse
from .models import Song, Announcement, UserActivity, Playlist, FavoriteSong
from django.contrib.auth.models import User


class SongModelTest(TestCase):
    def setUp(self):
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', file='test.mp3')

    def test_song_creation(self):
        self.assertEqual(self.song.title, 'Test Song')
        self.assertEqual(self.song.artist, 'Test Artist')
        self.assertEqual(str(self.song), 'Test Song')


class AnnouncementModelTest(TestCase):
    def setUp(self):
        self.announcement = Announcement.objects.create(title='Test Announcement', file='announcement.mp3')

    def test_announcement_creation(self):
        self.assertEqual(self.announcement.title, 'Test Announcement')
        self.assertEqual(str(self.announcement), 'Test Announcement')


class UserActivityModelTest(TestCase):
    def setUp(self):
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', file='test.mp3')
        self.user_activity = UserActivity.objects.create(name='Test User', store_name='Test Store', song=self.song)

    def test_user_activity_creation(self):
        self.assertEqual(self.user_activity.name, 'Test User')
        self.assertEqual(self.user_activity.store_name, 'Test Store')
        self.assertEqual(self.user_activity.song, self.song)
        self.assertEqual(str(self.user_activity),
                         f'{self.user_activity.name} - {self.user_activity.store_name} - {self.user_activity.song} - {self.user_activity.timestamp}')


class PlaylistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', file='test.mp3')
        self.playlist = Playlist.objects.create(user=self.user, name='Test Playlist')
        self.playlist.songs.add(self.song)

    def test_playlist_creation(self):
        self.assertEqual(self.playlist.name, 'Test Playlist')
        self.assertEqual(self.playlist.user.username, 'testuser')
        self.assertIn(self.song, self.playlist.songs.all())
        self.assertEqual(str(self.playlist), 'Test Playlist')


class FavoriteSongModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', file='test.mp3')
        self.favorite_song = FavoriteSong.objects.create(user=self.user, song=self.song)

    def test_favorite_song_creation(self):
        self.assertEqual(self.favorite_song.user.username, 'testuser')
        self.assertEqual(self.favorite_song.song.title, 'Test Song')
        self.assertEqual(str(self.favorite_song),
                         f'{self.favorite_song.user.username} - {self.favorite_song.song.title}')


class TrackActivityViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.song = Song.objects.create(title='Test Song', artist='Test Artist', file='test.mp3')
        self.announcement = Announcement.objects.create(title='Test Announcement', file='announcement.mp3', is_active=True)
        self.user_activity = UserActivity.objects.create(name='Test User', store_name='Test Store', song=self.song, current_time='00:00')
        self.url = reverse('track_activity')

    def test_track_activity_view(self):
        response = self.client.get(self.url, {'name': 'Test User', 'store_name': 'Test Store', 'song_id': self.song.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')
        self.assertContains(response, 'Test Store')
        self.assertContains(response, self.song.title)
        self.assertContains(response, self.announcement.title)

