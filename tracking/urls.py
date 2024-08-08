from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import track_activity, update_activity, update_current_time

router = DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'user-activities', views.UserActivityViewSet)

urlpatterns = [
    path('home/', views.home, name='home'),
    path('track/', track_activity, name='track_activity'),
    path('update_activity/', update_activity, name='update_activity'),
    path('update_activity_time/', views.update_activity_time, name='update_activity_time'),
    path('update_current_time/', update_current_time, name='update_current_time'),
    path('api/', include(router.urls)),
    re_path(r'^name=(?P<name>[^&]+)&store_name=(?P<store_name>[^&]+)$', views.track_activity_by_name_and_store, name='track_activity_by_name_and_store'),
]
