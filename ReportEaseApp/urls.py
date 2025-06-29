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
    path("evidence/<int:evidence_id>/<str:media_type>/", serve_decrypted_evidence, name= "serve_decrypted_evidence"),
    path("citizenship_photo/<int:citizenship_id>/", serve_decrypted_citizenship_photo, name="serve_decrypted_citizenship_photo"),
    path("recent_photo/<int:user_id>/", serve_decrypted_recent_photo, name="serve_decrypted_recent_photo"),
    path('chatmessages/<int:case_id>/', get_chat_messages, name='GetChatMessages'),
    path('notifications/', notification_view, name='Notifications'),
    path('fetchnotificationcount/', fetch_number_of_notifications,name="FetchNotificationCount"),
    path('mark_messages_read/<int:case_id>/',mark_messages_read,name = "MarkMessagesRead"),
    path('payments/', fetch_payments, name='FetchPayment'),
    path('createpayment/<int:case_id>/', create_payment, name='CreatePayment'),
    path('fetchpaymentscount/', fetchPaymentsCount, name='FetchPaymentsCount'),
    path('paypal/complete/', paypal_complete, name='paypal-complete'),
    path('khaltipayment/',khalti_payment,name='KhaltiPayment'),
    path('khalti/complete/', khalti_complete, name='KhaltiPaymentSuccess'),
]

# if settings.DEBUG:  # Serve media files only in development
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
