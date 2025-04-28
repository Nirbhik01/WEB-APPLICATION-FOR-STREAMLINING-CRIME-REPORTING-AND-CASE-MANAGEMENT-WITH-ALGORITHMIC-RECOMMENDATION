from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from .views import *

app_name = 'investigator'

urlpatterns = [
    path('uploadwanted/',UploadWanted, name='uploadwanted'), 
    path('markregistered/<int:id>/',mark_case_registered, name='mark_case_registered'),
    path("marknotregistered/<int:id>/",mark_case_not_registered,name="mark_case_not_registered"),# URL for the upload form
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)