from django.contrib import admin
from django.urls import path,include
from .views import * 
from django.conf.urls.static import static
from django.conf import settings
# from userauths.urls import *
# from userauths.views import *

app_name='ReportEaseApp'


urlpatterns = [
    path('' , LandingPage , name='LandingPage'),
    
    
    path('home/' , HomePage , name='HomePage'),
    path('caselist/' , CaseListPage , name='CaseListPage'),
    path('uploadwanted/' , UploadWantedPage , name='UploadWantedPage'),
    path('reviewfir/<int:id>/',ReviewFirPage,name='ReviewFirPage'),
    path('casepage/<int:id>/' , CasePage , name='CasePage'),
    path('reportcrime/' , ReportCrimePage , name='ReportCrimePage'),
    path('casedetails/<int:id>/',case_details, name='CaseDetails'),
    path('casestatus/<int:id>/',case_status, name='CaseStatus'),
    path('activitylog/<int:id>/', activity_log , name='ActivityLog'),
    path('fetchactivitylog/<int:id>/',fetch_activity_log,name="FetchActivityLog"),
    # path('case/',include('Case.urls')),
    
    # path('logout/' , LogoutPage , name='LogoutPage'),
    path('profile/' , ProfilePage , name='ProfilePage'),
    # path('settings/' , SettingsPage , name='SettingsPage'),
    # path('account/' , AccountPage , name='AccountPage'),
]

# if settings.DEBUG:  # Serve media files only in development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
