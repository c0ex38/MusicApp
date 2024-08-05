from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Song(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Başlık"))
    artist = models.CharField(max_length=255, verbose_name=_("Sanatçı"))
    file = models.FileField(upload_to='songs/', verbose_name=_("Dosya"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Tarihi"))

    def __str__(self):
        return self.title


class UserActivity(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Ad"))
    store_name = models.CharField(max_length=255, verbose_name=_("Mağaza Adı"))
    last_active = models.DateTimeField(auto_now=True, verbose_name=_("Son Aktivite"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Zaman Damgası"))
    song = models.ForeignKey(Song, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Şarkı"))
    current_time = models.CharField(max_length=10, default='00:00', verbose_name=_("Şu Anki Zaman"))

    def __str__(self):
        return f"{self.name} - {self.store_name} - {self.song} - {self.timestamp}"


class Announcement(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Başlık"))
    file = models.FileField(upload_to='announcements/', verbose_name=_("Dosya"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Tarihi"))
    interval = models.PositiveIntegerField(default=3, verbose_name=_("Aralık"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktif"))

    def __str__(self):
        return self.title


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    songs = models.ManyToManyField(Song)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FavoriteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"
