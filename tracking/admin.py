from django.contrib import admin
from .models import Playlist, FavoriteSong, UserActivity, Song, Announcement


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_name', 'song', 'current_time', 'last_active', 'timestamp')
    list_filter = ('name', 'timestamp', 'song')


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_at')
    list_filter = ('artist', 'created_at')


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'interval', 'is_active', 'created_at')
    list_filter = ('created_at', 'is_active')
    list_editable = ('interval', 'is_active')


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at')
    list_filter = ('user', 'created_at')


@admin.register(FavoriteSong)
class FavoriteSongAdmin(admin.ModelAdmin):
    list_display = ('user', 'song', 'added_at')
    list_filter = ('user', 'added_at')
