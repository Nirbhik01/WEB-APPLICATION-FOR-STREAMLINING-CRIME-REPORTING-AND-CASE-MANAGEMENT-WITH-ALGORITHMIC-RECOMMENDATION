from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('' , LandingPage , name='LandingPage'),
    path('login/' , LoginPage , name='LoginPage'),
    path('register/' , RegisterPage , name='RegisterPage'),
    path('home/' , HomePage , name='HomePage'),
    path('caselist/' , CaseListPage , name='CaseListPage'),
    path('uploadwanted/' , UploadWantedPage , name='UploadWantedPage'),
    path('reviewfir/<int:id>',ReviewFirPage,name='ReviewFirPage'),
    path('case/' , CasePage , name='CasePage'),
    path('reportcrime/' , ReportCrimePage , name='ReportCrimePage'),
    
    # path('logout/' , LogoutPage , name='LogoutPage'),
    path('profile/' , ProfilePage , name='ProfilePage'),
    # path('settings/' , SettingsPage , name='SettingsPage'),
    # path('account/' , AccountPage , name='AccountPage'),
]
