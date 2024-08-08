import random

from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.timezone import now, timedelta
from django.utils.translation import gettext_lazy as _

from .models import Playlist, FavoriteSong, UserActivity, Song, Announcement

admin.site.site_header = _("DGN Müzik Yönetimi")  # Burada kendi başlığınızı yazabilirsiniz
admin.site.site_title = _("DGN Müzik")


class StoreNameFilter(admin.SimpleListFilter):
    title = 'Mağaza Adı'
    parameter_name = 'store_name'

    def lookups(self, request, model_admin):
        store_names = set([c.store_name for c in model_admin.model.objects.all()])
        return [(store_name, store_name) for store_name in store_names]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(store_name=self.value())
        return queryset


class IsActiveFilter(admin.SimpleListFilter):
    title = 'Aktiflik Durumu'
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return [
            ('active', 'Aktif'),
            ('inactive', 'Pasif'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)
        return queryset


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'store_name', 'song', 'current_time', 'is_active')
    change_list_template = "admin/change_list.html"
    list_filter = (StoreNameFilter, IsActiveFilter)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        for activity in qs:
            if now() - activity.last_active > timedelta(seconds=10):
                activity.is_active = False
                activity.save()
        return qs

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        queryset = self.get_queryset(request)

        # Mağaza adına göre gruplama
        grouped_queryset = {}
        for activity in queryset:
            store = activity.store_name
            if store not in grouped_queryset:
                grouped_queryset[store] = []
            grouped_queryset[store].append(activity)

        extra_context['grouped_queryset'] = grouped_queryset
        return super(UserActivityAdmin, self).changelist_view(request, extra_context=extra_context)


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'created_at')
    change_list_template = "admin/tracking/song_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('shuffle/', self.admin_site.admin_view(self.shuffle_songs), name='shuffle-songs'),
        ]
        return custom_urls + urls

    def shuffle_songs(self, request):
        songs = list(Song.objects.all())
        random.shuffle(songs)
        for index, song in enumerate(songs):
            song.order = index
            song.save()
        self.message_user(request, "Şarkılar karıştırıldı.")
        return HttpResponseRedirect("../")


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
