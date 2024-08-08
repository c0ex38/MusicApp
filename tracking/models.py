from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    file = models.FileField(upload_to='songs/')
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']


class UserActivity(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Ad"))
    store_name = models.CharField(max_length=255, verbose_name=_("Mağaza Adı"), blank=True, null=True)
    song = models.CharField(max_length=255, verbose_name=_("Şarkı"), default="Bilinmeyen Şarkı")
    last_active = models.DateTimeField(auto_now=True, verbose_name=_("Son Aktivite"))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Zaman Damgası"))
    current_time = models.CharField(max_length=10, default='00:00', verbose_name=_("Şu Anki Zaman"))
    is_active = models.BooleanField(default=True, verbose_name=_("Aktif"))

    def save(self, *args, **kwargs):
        if not self.song:
            self.song = self.get_current_song()
        super(UserActivity, self).save(*args, **kwargs)

    def get_current_song(self):
        return self.song

    @property
    def current_track_title(self):
        return self.song



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
    name = models.CharField(max_length=255, verbose_name=_("Ad"))
    songs = models.ManyToManyField(Song, verbose_name=_("Şarkılar"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Oluşturulma Tarihi"))

    def __str__(self):
        return self.name


class FavoriteSong(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Eklenme Tarihi"))

    def __str__(self):
        return f"{self.user.username} - {self.song.title}"
