from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .views import fetch_cases,search_cases,filter_cases,display_cases

urlpatterns = [
    path('getcases/', fetch_cases, name='fetch_cases'),
    path('searchcases/', search_cases, name='search_cases'),
    path('filtercases/', filter_cases, name='filter_cases'),
    path('displaycases/',display_cases,name="display_cases")
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)