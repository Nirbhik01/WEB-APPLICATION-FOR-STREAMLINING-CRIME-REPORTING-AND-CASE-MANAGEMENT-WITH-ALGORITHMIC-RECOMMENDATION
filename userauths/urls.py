from django.urls import path,include
from .views import *

app_name='userauths'

urlpatterns=[
    path('', redirect_to_login , name='redirect'),
    path('login/' , LoginPage , name='LoginPage'),
    path('register/' , RegisterPage , name='RegisterPage'),
     path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('change-password/', change_password, name='change_password'),
    path('forgotpassword/' , ForgotPasswordPage , name='ForgotPasswordPage'),
    path('logout/' , LogoutPage , name='LogoutPage'),
]