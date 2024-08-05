from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'songs', views.SongViewSet)
router.register(r'user-activities', views.UserActivityViewSet)

urlpatterns = [
    path('home/', views.home, name='home'),
    path('track/', views.track_activity, name='track_activity'),
    path('api/', include(router.urls)),
]
