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
    path('reviewfir/<int:id>/' , ReviewFirPage , name='ReviewFirPage'),
    path('casepage/<int:id>/' , CasePage , name='CasePage'),
    path('reportcrime/' , ReportCrimePage , name='ReportCrimePage'),
    path('casedetails/<int:id>/' , case_details , name='CaseDetails'),
    path('terminatedcasedetails/' , fetch_terminated_case_details , name='TerminatedCaseDetails'),
    path('casestatus/<int:id>/' , case_status , name='CaseStatus'),
    path('activitylog/<int:id>/' , activity_log , name='ActivityLog'),
    path('fetchactivitylog/<int:id>/', fetch_activity_log,name="FetchActivityLog"),
    path('editprofiledetails/' , EditProfilePage , name='EditProfilePage'),
    path('fetchuserdetails/', fetch_user_details , name='FetchUserDetails'),
    path('profile/' , ProfilePage , name='ProfilePage'),
    path('updateprofile/',save_edited_user_details, name='SaveEditedUserDetails'),
    path('assigninvestigator/<int:id>/', assign_investigator, name='AssignInvestigator'),
    path('successfullyterminated/<int:id>/', mark_case_successfully_terminated, name = 'SuccessfullyTerminated'),
    path('unsuccessfullyterminated/<int:id>/', mark_case_unsuccessfully_terminated, name = 'UnsuccessfullyTerminated'),
    path("evidence/<int:evidence_id>/<str:media_type>/", serve_decrypted_evidence, name= "serve_decrypted_evidence")
]

# if settings.DEBUG:  # Serve media files only in development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
