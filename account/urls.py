from .views import *

from django.urls import path

app_name = 'account'

urlpatterns = [
    # registration
    path('register/',register_user,name='register'),
    path('email-verification-sent/',email_verification_sent,name='email-verification-sent'),
]