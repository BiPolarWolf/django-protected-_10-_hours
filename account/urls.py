from .views import *

from django.urls import path

app_name = 'account'

urlpatterns = [
    # registration
    path('register/',register_user,name='register'),
    path('email-verification-sent/',email_verification_sent,name='email-verification-sent'),

    # login and logout

    path('login/',login_user,name='login'),
    path('logout/',logout_user,name='logout'),


    # dashboard
    path('dashboard/',dashboard_user,name='dashboard'),
    path('profile-management/',profile_management,name='profile-management'),
    path('delete_user/',delete_user,name='delete-user'),


]