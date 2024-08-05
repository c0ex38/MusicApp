from rest_framework import serializers
from .models import Song, Playlist, FavoriteSong, UserActivity

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'file', 'created_at']

class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'user', 'name', 'songs', 'created_at']

class FavoriteSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteSong
        fields = ['id', 'user', 'song', 'added_at']

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'name', 'store_name', 'last_active', 'timestamp', 'song']
