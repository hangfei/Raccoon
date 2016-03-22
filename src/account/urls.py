from __future__ import unicode_literals

from django.conf.urls import url

from account.views import ClientSignupView, ConsultantSignupView, LoginView, LogoutView, DeleteView
from account.views import ConfirmEmailView
from account.views import ChangePasswordView, PasswordResetView, PasswordResetTokenView
from account.views import SettingsView

from . import views

urlpatterns = [
    url(r'^set_language/$', views.set_account_language, name='set_account_language'),
    url(r'^signup/$', views.sign_up, name='account_sign_up'),
    url(r"^signup/client/$", ClientSignupView.as_view(), name="client_account_signup"),
    url(r"^signup/expert/$", ConsultantSignupView.as_view(), name="consultant_account_signup"),
    url(r"^login/$", LoginView.as_view(), name="account_login"),
    url(r"^logout/$", LogoutView.as_view(), name="account_logout"),
    url(r"^confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
    url(r"^password/$", ChangePasswordView.as_view(), name="account_password"),
    url(r"^password/reset/$", PasswordResetView.as_view(), name="account_password_reset"),
    url(r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", PasswordResetTokenView.as_view(), name="account_password_reset_token"),
    url(r"^settings/$", SettingsView.as_view(), name="account_settings"),
    url(r"^delete/$", DeleteView.as_view(), name="account_delete"),
]
