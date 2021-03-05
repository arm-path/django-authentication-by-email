from django.urls import re_path, path

from django_users.services import check_email_registration, check_email_authorization
from django_users.views import AuthorizationView, RegistrationView, LogoutSystemView, \
    PasswordResetSendEmailView, PasswordResetChangePassword, verification, system_and_logout_view

urlpatterns = [
    path('', AuthorizationView.as_view(), name='authorization'),
    path('', LogoutSystemView.as_view(), name='logout'),
    path('registartion/', RegistrationView.as_view(), name='registration'),
    path('password-reset/', PasswordResetSendEmailView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', PasswordResetChangePassword.as_view(), name='password_reset_confirm'),
    path('system/', system_and_logout_view, name='system'),
    re_path(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verification, name='verification'),

    path('check_email_registration/', check_email_registration, name='check_email_registration'),
    path('check_email_authorization/', check_email_authorization, name='check_email_authorization'),
]
