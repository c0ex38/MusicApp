from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tracking.views import update_activity
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracking.urls')),  # Root URL
    path('update_activity/', update_activity, name='update_activity'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
