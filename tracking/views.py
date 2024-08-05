from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Song, Announcement, UserActivity
from rest_framework import viewsets
from .serializers import SongSerializer, UserActivitySerializer


def home(request):
    # Otomatik yönlendirme için gerekli parametreler
    name = request.GET.get('name', 'testuser')
    store_name = request.GET.get('store_name', 'teststore')
    return redirect(f'/tracking/track/?name={name}&store_name={store_name}')

def track_activity(request):
    name = request.GET.get('name')
    store_name = request.GET.get('store_name')
    song_id = request.GET.get('song_id')

    if song_id:
        song = Song.objects.get(id=song_id)
    else:
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

    songs = Song.objects.all()
    announcements = Announcement.objects.filter(is_active=True)

    return render(request, 'track_activity.html', {
        'name': name,
        'store_name': store_name,
        'songs': songs,
        'announcements': announcements,
    })

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer


class UserActivityViewSet(viewsets.ModelViewSet):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
