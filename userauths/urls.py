from django.urls import path,include
from .views import *

app_name='userauths'

urlpatterns=[
    path('', redirect_to_login , name='redirect'),
    path('login/' , LoginPage , name='LoginPage'),
    path('register/' , RegisterPage , name='RegisterPage'),
    path('logout/' , LogoutPage , name='LogoutPage'),
]