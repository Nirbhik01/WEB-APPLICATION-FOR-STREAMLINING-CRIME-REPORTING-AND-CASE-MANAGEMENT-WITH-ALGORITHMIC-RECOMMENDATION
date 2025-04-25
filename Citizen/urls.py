from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .views import register_case

urlpatterns = [
    path('registercase/', register_case, name='register_case'),
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)