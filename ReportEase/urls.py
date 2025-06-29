"""
URL configuration for ReportEase project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ReportEaseApp.urls')),
    path('',include('ReportEaseApp.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path("user/", include("userauths.urls", namespace="userauths")),
    path('case/', include('Case.urls')),
    path('investigator/', include('Investigator.urls')),  
    path('citizen/', include('Citizen.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    path('khalti/', include('khalti.urls')),
]

if settings.DEBUG:  # Serve media files only in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)