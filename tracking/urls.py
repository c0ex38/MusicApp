from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'user-activities', views.UserActivityViewSet)

urlpatterns = [
    path('home/', views.home, name='home'),
    path('track/', views.track_activity, name='track_activity'),
    path('api/', include(router.urls)),
    re_path(r'^name=(?P<name>[^&]+)&store_name=(?P<store_name>[^&]+)$', views.track_activity_by_name_and_store, name='track_activity_by_name_and_store'),
]
