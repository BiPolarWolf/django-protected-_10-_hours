from re import template
from django.contrib.messages import success
from .views import *
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from django.urls import path, reverse_lazy
from .views import *

app_name = "account"

urlpatterns = [
    # registration
    path("register/", register_user, name="register"),
    path(
        "email-verification-sent/",
        email_verification_sent,
        name="email-verification-sent",
    ),
    # login and logout
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    # dashboard
    path("dashboard/", dashboard_user, name="dashboard"),
    path("profile-management/", profile_management, name="profile-management"),
    path("delete_user/", delete_user, name="delete-user"),
    # password reset
    path(
        "password-reset",
        auth_views.PasswordResetView.as_view(
            template_name="account/password/password_reset.html",
            email_template_name="account/password/password_reset_email.html",
            success_url=reverse_lazy("account:password-reset-done"),
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/password/password_reset_done.html"
        ),
        name="password-reset-done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/password/password_reset_confirm.html",
            success_url=reverse_lazy("account:password-reset-complete"),
        ),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="account/password/password_reset_complete.html"
        ),
        name="password-reset-complete",
    ),
]
