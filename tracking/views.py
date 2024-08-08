import json
from urllib.parse import urlencode

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

from .models import Song, Announcement, UserActivity
from .serializers import SongSerializer, UserActivitySerializer

def home(request):
    name = request.GET.get('name', 'testuser')
    store_name = request.GET.get('store_name', 'teststore')
    query_params = urlencode({'name': name, 'store_name': store_name})
    return redirect(f'/track/?{query_params}')

@csrf_exempt
def track_activity(request):
    name = request.GET.get('name')
    store_name = request.GET.get('store_name')
    song_id = request.GET.get('song_id')

    try:
        song = Song.objects.get(id=song_id)
    except Song.DoesNotExist:
        song = None

    user_activity, created = UserActivity.objects.get_or_create(
        name=name,
        store_name=store_name,
        defaults={'song': song.title if song else 'Bilinmeyen Şarkı', 'last_active': timezone.now(), 'current_time': '00:00'}
    )

    if not created:
        user_activity.song = song.title if song else 'Bilinmeyen Şarkı'
        user_activity.last_active = timezone.now()
        user_activity.is_active = True
        user_activity.save()

    context = {
        'songs': Song.objects.all(),
        'announcements': Announcement.objects.filter(is_active=True),
        'current_song_id': song_id,
        'current_time': user_activity.current_time
    }

    return render(request, 'tracking/track_activity.html', context)

@csrf_exempt
def update_current_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        store_name = data.get('store_name')
        current_time = data.get('current_time')

        try:
            user_activity = UserActivity.objects.get(name=name, store_name=store_name)
            user_activity.current_time = current_time
            user_activity.last_active = timezone.now()
            user_activity.is_active = True
            user_activity.save()
            return JsonResponse({'status': 'success'})
        except UserActivity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'UserActivity not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt
def update_activity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        store_name = data.get('store_name')
        song_id = data.get('song_id')

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            song = None

        user_activity, created = UserActivity.objects.get_or_create(
            name=name,
            store_name=store_name,
            defaults={'song': song.title if song else 'Bilinmeyen Şarkı', 'last_active': timezone.now(), 'current_time': '00:00'}
        )

        if not created:
            user_activity.song = song.title if song else 'Bilinmeyen Şarkı'
            user_activity.last_active = timezone.now()
            user_activity.is_active = True
            user_activity.save()

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)

@csrf_exempt
def update_activity_time(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data['name']
        store_name = data['store_name']
        song_id = data['song_id']
        current_time = data['current_time']

        try:
            user_activity = UserActivity.objects.get(
                name=name,
                store_name=store_name
            )
            user_activity.current_time = current_time
            user_activity.last_active = timezone.now()
            user_activity.is_active = True
            user_activity.save()
            return JsonResponse({'status': 'success'})
        except UserActivity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User activity not found'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def track_activity_by_name_and_store(request, name, store_name):
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
        user_activity.is_active = True
        user_activity.save()

    songs = Song.objects.all()
    announcements = Announcement.objects.filter(is_active=True)

    return render(request, 'tracking/track_activity.html', {
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
