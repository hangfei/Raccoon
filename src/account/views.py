from __future__ import unicode_literals

from django.http import Http404, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.utils.http import base36_to_int, int_to_base36
from django.core.urlresolvers import reverse
from django.core.files import File
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import FormView

from django.contrib import auth, messages
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator

from account import signals
from account.conf import settings
from account.forms import ConsultantSignupForm, ClientSignupForm, LoginUsernameForm
from account.forms import ChangePasswordForm, PasswordResetForm, PasswordResetTokenForm
from account.forms import SettingsForm
from account.hooks import hookset
from account.mixins import LoginRequiredMixin
from common.models import UserProfile, Client, Expert, SignupCode, EmailAddress, EmailConfirmation, Account, AccountDeletion
from account.utils import default_redirect, get_form_data

from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render
from django.contrib import messages
import requests
import urllib.request
import os

def sign_up(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'account/sign_up.html', context)

# Account app will override the language code in django itself.
# https://github.com/pinax/django-user-accounts/blob/master/account/middleware.py
def set_account_language(request):
    if request.method == 'POST':
        language = request.POST.get('language', '')
        supported_languages = [language_pair[0] for language_pair in settings.LANGUAGES]
        if request.user.is_authenticated() and language and language in supported_languages:
            try:
                account = Account.objects.get(user=request.user)
                account.language = language
                account.save()
            except Account.DoesNotExist:
                return HttpResponse(status=404)

        return HttpResponse(status=204)
    return HttpResponse(status=400)

def handle_uploaded_file(form, request, username, created_profile):
    file_type_suffix = 'jpg'
    image_name = str(username)
    file_name = image_name + "." + file_type_suffix
    file_path = 'media/' + file_name
    if not form.cleaned_data['profile_image'] and 'linkedin_profile_image' in request.session:
        result = urllib.request.urlretrieve(request.session['linkedin_profile_image'], file_path)
        created_profile.avatar.save(
            os.path.basename(username),
            File(open(result[0], 'rb'))
        )
        created_profile.save()

class ClientSignupView(FormView):

    template_name = "account/signup_client.html"
    template_name_ajax = "account/ajax/signup.html"
    template_name_email_confirmation_sent = "account/email_confirmation_sent.html"
    template_name_email_confirmation_sent_ajax = "account/ajax/email_confirmation_sent.html"
    template_name_signup_closed = "account/signup_closed.html"
    template_name_signup_closed_ajax = "account/ajax/signup_closed.html"
    form_class = ClientSignupForm
    form_kwargs = {}
    redirect_field_name = "next"
    identifier_field = "username"
    messages = {
        "email_confirmation_sent": {
            "level": messages.INFO,
            "text": _("Confirmation email sent to {email}.")
        },
        "invalid_signup_code": {
            "level": messages.WARNING,
            "text": _("The code {code} is invalid.")
        }
    }

    def __init__(self, *args, **kwargs):
        self.created_user = None
        kwargs["signup_code"] = None
        super(ClientSignupView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.setup_signup_code()
        return super(ClientSignupView, self).dispatch(request, *args, **kwargs)

    def setup_signup_code(self):
        code = self.get_code()
        if code:
            try:
                self.signup_code = SignupCode.check_code(code)
            except SignupCode.InvalidCode:
                self.signup_code = None
            self.signup_code_present = True
        else:
            self.signup_code = None
            self.signup_code_present = False

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(default_redirect(self.request, settings.ACCOUNT_LOGIN_REDIRECT_URL))
        if not self.is_open():
            return self.closed()
        return super(ClientSignupView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            raise Http404()
        if not self.is_open():
            return self.closed()
        return super(ClientSignupView, self).post(*args, **kwargs)

    def get_initial(self):
        initial = super(ClientSignupView, self).get_initial()
        if self.signup_code:
            initial["code"] = self.signup_code.code
            if self.signup_code.email:
                initial["email"] = self.signup_code.email
        return initial

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = super(ClientSignupView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(ClientSignupView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        signals.user_sign_up_attempt.send(
            sender=ClientSignupForm,
            username=get_form_data(form, self.identifier_field),
            email=get_form_data(form, "email"),
            result=form.is_valid()
        )
        return super(ClientSignupView, self).form_invalid(form)

    def form_valid(self, form):
        self.created_user = self.create_user(form, commit=False)
        # prevent User post_save signal from creating an Account instance
        # we want to handle that ourself.
        self.created_user._disable_account_creation = True
        self.created_user.save()
        group = Group.objects.get(name='client')
        self.created_user.groups.add(group)
        self.use_signup_code(self.created_user)
        email_address = self.create_email_address(form)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED and not email_address.verified:
            self.created_user.is_active = False
            self.created_user.save()
        self.create_account(form)
        self.create_client(form)
        self.create_profile(form)


        self.after_signup(form)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL and not email_address.verified:
            self.send_email_confirmation(email_address)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED and not email_address.verified:
            return self.email_confirmation_required_response()
        else:
            show_message = [
                settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL,
                self.messages.get("email_confirmation_sent"),
                not email_address.verified
            ]
            if all(show_message):
                messages.add_message(
                    self.request,
                    self.messages["email_confirmation_sent"]["level"],
                    self.messages["email_confirmation_sent"]["text"].format(**{
                        "email": form.cleaned_data["email"]
                    })
                )
            # attach form to self to maintain compatibility with login_user
            # API. this should only be relied on by d-u-a and it is not a stable
            # API for site developers.
            self.form = form
            self.login_user()
        return redirect(self.get_success_url())

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_SIGNUP_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def create_user(self, form, commit=True, model=None, **kwargs):
        User = model
        if User is None:
            User = get_user_model()
        user = User(**kwargs)
        username = form.cleaned_data.get("username")
        if username is None:
            username = self.generate_username(form)
        user.username = username
        user.email = form.cleaned_data["email"].strip()
        password = form.cleaned_data.get("password")
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    def create_account(self, form):
        return Account.create(request=self.request, user=self.created_user, create_email=False)

    def create_client(self, form):
        return Client.create(form, request=self.request, user=self.created_user)

    def create_profile(self, form):
        return UserProfile.create(form, request=self.request, user=self.created_user, user_type="CLIENT")

    def generate_username(self, form):
        raise NotImplementedError(
            "Unable to generate username by default. "
            "Override SignupView.generate_username in a subclass."
        )

    def create_email_address(self, form, **kwargs):
        kwargs.setdefault("primary", True)
        kwargs.setdefault("verified", False)
        if self.signup_code:
            kwargs["verified"] = self.signup_code.email and self.created_user.email == self.signup_code.email
        return EmailAddress.objects.add_email(self.created_user, self.created_user.email, **kwargs)

    def use_signup_code(self, user):
        if self.signup_code:
            self.signup_code.use(user)

    def send_email_confirmation(self, email_address):
        email_address.send_confirmation(site=get_current_site(self.request))

    def after_signup(self, form):
        signals.user_signed_up.send(sender=ClientSignupForm, user=self.created_user, form=form)

    def login_user(self):
        user = self.created_user
        if settings.ACCOUNT_USE_AUTH_AUTHENTICATE:
            # call auth.authenticate to ensure we set the correct backend for
            # future look ups using auth.get_user().
            user = auth.authenticate(**self.user_credentials())
        else:
            # set auth backend to ModelBackend, but this may not be used by
            # everyone. this code path is deprecated and will be removed in
            # favor of using auth.authenticate above.
            user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def user_credentials(self):
        return hookset.get_user_credentials(self.form, self.identifier_field)

    def get_code(self):
        return self.request.POST.get("code", self.request.GET.get("code"))

    def is_open(self):
        # TODO Turn off singup code to remove code invalid warning
        if settings.ACCOUNT_USE_SINGUP_CODE:
            if self.signup_code:
                return True
            else:
                if self.signup_code_present:
                    if self.messages.get("invalid_signup_code"):
                        messages.add_message(
                            self.request,
                            self.messages["invalid_signup_code"]["level"],
                            self.messages["invalid_signup_code"]["text"].format(**{
                                "code": self.get_code(),
                            })
                        )
        else:
            return settings.ACCOUNT_OPEN_SIGNUP

    def email_confirmation_required_response(self):
        if self.request.is_ajax():
            template_name = self.template_name_email_confirmation_sent_ajax
        else:
            template_name = self.template_name_email_confirmation_sent
        response_kwargs = {
            "request": self.request,
            "template": template_name,
            "context": {
                "email": self.created_user.email,
                "success_url": self.get_success_url(),
            }
        }
        return self.response_class(**response_kwargs)

    def closed(self):
        if self.request.is_ajax():
            template_name = self.template_name_signup_closed_ajax
        else:
            template_name = self.template_name_signup_closed
        response_kwargs = {
            "request": self.request,
            "template": template_name,
        }
        return self.response_class(**response_kwargs)

class ConsultantSignupView(FormView):

    template_name = "account/signup_consultant.html"
    template_name_ajax = "account/ajax/signup.html"
    template_name_email_confirmation_sent = "account/email_confirmation_sent.html"
    template_name_email_confirmation_sent_ajax = "account/ajax/email_confirmation_sent.html"
    template_name_signup_closed = "account/signup_closed.html"
    template_name_signup_closed_ajax = "account/ajax/signup_closed.html"
    form_class = ConsultantSignupForm
    form_kwargs = {}
    redirect_field_name = "next"
    identifier_field = "username"
    messages = {
        "email_confirmation_sent": {
            "level": messages.INFO,
            "text": _("Confirmation email sent to {email}.")
        },
        "invalid_signup_code": {
            "level": messages.WARNING,
            "text": _("The code {code} is invalid.")
        }
    }

    def __init__(self, *args, **kwargs):
        self.created_user = None
        kwargs["signup_code"] = None
        super(ConsultantSignupView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.setup_signup_code()
        return super(ConsultantSignupView, self).dispatch(request, *args, **kwargs)

    def setup_signup_code(self):
        code = self.get_code()
        if code:
            try:
                self.signup_code = SignupCode.check_code(code)
            except SignupCode.InvalidCode:
                self.signup_code = None
            self.signup_code_present = True
        else:
            self.signup_code = None
            self.signup_code_present = False

    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated():
            return redirect(default_redirect(self.request, settings.ACCOUNT_LOGIN_REDIRECT_URL))
        if not self.is_open():
            return self.closed()
        request = args[0]
        redirect_domain = 'http://' + request.META['HTTP_HOST']
        # reset form for each request
        self.form_kwargs['initial'] = {}
        self.request.session['linkedin_profile_image'] = None
        if request.GET.get('code'):
            post_data = {'grant_type':'authorization_code',
                         'code':request.GET.get('code'),
                         'redirect_uri': redirect_domain + '/account/signup/expert/',
                         'client_id': '75y73411x5u1zu',
                         'client_secret': '57dIUusbTq2I5G2E',
                        }    # a sequence of two element tuples
            headers = {'Host': 'www.linkedin.com', 'Content-Type': 'application/x-www-form-urlencoded'}

            result = requests.post("https://www.linkedin.com/uas/oauth2/accessToken", post_data, headers=headers)

            get_headers = {'Host': 'api.linkedin.com', 'Connection':'Keep-Alive', 'Authorization': 'Bearer ' + result.json()['access_token']}
            profile_fields = '(id,firstName,lastName,positions,headline,specialties,summary,num-connections,picture-url,picture-urls::(original))'
            get_result = requests.get("https://api.linkedin.com/v1/people/~:" + profile_fields + "?format=json", headers=get_headers)

            initial_data = {}
            if 'firstName' in get_result.json():
                initial_data['first_name'] = get_result.json()['firstName']
            if 'lastName' in get_result.json():
                initial_data['last_name'] = get_result.json()['lastName']
            if 'summary' in get_result.json():
                initial_data['description_text'] = get_result.json()['summary']

            self.form_kwargs['initial'] = initial_data
            if 'pictureUrls' in get_result.json():
                if 'values' in get_result.json()['pictureUrls']:
                    if get_result.json()['pictureUrls']['values']:
                        self.request.session['linkedin_profile_image'] = get_result.json()['pictureUrls']['values'][0]

            # return super(ConsultantSignupView, self).get(*args, **kwargs)
            ctx = super(ConsultantSignupView, self).get_context_data(**kwargs)
            ctx.update({
                'linkedin_signup': True,
            })
            return self.render_to_response(ctx)
        else:
            base_authorization_url = 'https://www.linkedin.com/uas/oauth2/authorization?response_type=code&client_id=75y73411x5u1zu&redirect_uri='
            redirect_url  = redirect_domain + '/account/signup/expert/'
            state = '&state=987654321'
            permissions = '&scope=r_basicprofile'
            linkedin_api_link = base_authorization_url + redirect_url + state + permissions
            ctx = super(ConsultantSignupView, self).get_context_data(**kwargs)
            ctx.update({
                'linkedin_api_link': linkedin_api_link,
            })
            return self.render_to_response(ctx)


    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            raise Http404()
        if not self.is_open():
            return self.closed()
        return super(ConsultantSignupView, self).post(*args, **kwargs)

    def get_initial(self):
        initial = super(ConsultantSignupView, self).get_initial()
        if self.signup_code:
            initial["code"] = self.signup_code.code
            if self.signup_code.email:
                initial["email"] = self.signup_code.email
        return initial

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = super(ConsultantSignupView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(ConsultantSignupView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        signals.user_sign_up_attempt.send(
            sender=ConsultantSignupForm,
            username=get_form_data(form, self.identifier_field),
            email=get_form_data(form, "email"),
            result=form.is_valid()
        )
        return super(ConsultantSignupView, self).form_invalid(form)

    def form_valid(self, form):
        self.created_user = self.create_user(form, commit=False)
        # prevent User post_save signal from creating an Account instance
        # we want to handle that ourself.
        self.created_user._disable_account_creation = True
        self.created_user.save()
        group = Group.objects.get(name='expert')
        self.created_user.groups.add(group)
        self.use_signup_code(self.created_user)
        email_address = self.create_email_address(form)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED and not email_address.verified:
            self.created_user.is_active = False
            self.created_user.save()
        self.create_account(form)
        self.create_consultant(form)
        created_profile = self.create_profile(form)

        if self.request.method == 'POST':
            handle_uploaded_file(form, self.request, self.created_user.username, created_profile)

        self.after_signup(form)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL and not email_address.verified:
            self.send_email_confirmation(email_address)
        if settings.ACCOUNT_EMAIL_CONFIRMATION_REQUIRED and not email_address.verified:
            return self.email_confirmation_required_response()
        else:
            show_message = [
                settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL,
                self.messages.get("email_confirmation_sent"),
                not email_address.verified
            ]
            if all(show_message):
                messages.add_message(
                    self.request,
                    self.messages["email_confirmation_sent"]["level"],
                    self.messages["email_confirmation_sent"]["text"].format(**{
                        "email": form.cleaned_data["email"]
                    })
                )
            # attach form to self to maintain compatibility with login_user
            # API. this should only be relied on by d-u-a and it is not a stable
            # API for site developers.
            self.form = form
            self.login_user()
        return redirect(self.get_success_url())

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_SIGNUP_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def create_user(self, form, commit=True, model=None, **kwargs):
        User = model
        if User is None:
            User = get_user_model()
        user = User(**kwargs)
        username = form.cleaned_data.get("username")
        if username is None:
            username = self.generate_username(form)
        user.username = username
        user.email = form.cleaned_data["email"].strip()
        password = form.cleaned_data.get("password")
        user.first_name = form.cleaned_data.get("first_name")
        user.last_name = form.cleaned_data.get("last_name")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user

    def create_account(self, form):
        return Account.create(request=self.request, user=self.created_user, create_email=False)

    def create_consultant(self, form):
        return Expert.create(form, request=self.request, user=self.created_user)

    def create_profile(self, form):
        return UserProfile.create(form, request=self.request, user=self.created_user, user_type="EXPERT")

    def generate_username(self, form):
        raise NotImplementedError(
            "Unable to generate username by default. "
            "Override SignupView.generate_username in a subclass."
        )

    def create_email_address(self, form, **kwargs):
        kwargs.setdefault("primary", True)
        kwargs.setdefault("verified", False)
        if self.signup_code:
            kwargs["verified"] = self.signup_code.email and self.created_user.email == self.signup_code.email
        return EmailAddress.objects.add_email(self.created_user, self.created_user.email, **kwargs)

    def use_signup_code(self, user):
        if self.signup_code:
            self.signup_code.use(user)

    def send_email_confirmation(self, email_address):
        email_address.send_confirmation(site=get_current_site(self.request))

    def after_signup(self, form):
        signals.user_signed_up.send(sender=ConsultantSignupForm, user=self.created_user, form=form)

    def login_user(self):
        user = self.created_user
        if settings.ACCOUNT_USE_AUTH_AUTHENTICATE:
            # call auth.authenticate to ensure we set the correct backend for
            # future look ups using auth.get_user().
            user = auth.authenticate(**self.user_credentials())
        else:
            # set auth backend to ModelBackend, but this may not be used by
            # everyone. this code path is deprecated and will be removed in
            # favor of using auth.authenticate above.
            user.backend = "django.contrib.auth.backends.ModelBackend"
        auth.login(self.request, user)
        self.request.session.set_expiry(0)

    def user_credentials(self):
        return hookset.get_user_credentials(self.form, self.identifier_field)

    def get_code(self):
        return self.request.POST.get("code", self.request.GET.get("code"))

    def is_open(self):
        # TODO Turn off singup code to remove code invalid warning
        if settings.ACCOUNT_USE_SINGUP_CODE:
            if self.signup_code:
                return True
            else:
                if self.signup_code_present:
                    if self.messages.get("invalid_signup_code"):
                        messages.add_message(
                            self.request,
                            self.messages["invalid_signup_code"]["level"],
                            self.messages["invalid_signup_code"]["text"].format(**{
                                "code": self.get_code(),
                            })
                        )
        else:
            return settings.ACCOUNT_OPEN_SIGNUP

    def email_confirmation_required_response(self):
        if self.request.is_ajax():
            template_name = self.template_name_email_confirmation_sent_ajax
        else:
            template_name = self.template_name_email_confirmation_sent
        response_kwargs = {
            "request": self.request,
            "template": template_name,
            "context": {
                "email": self.created_user.email,
                "success_url": self.get_success_url(),
            }
        }
        return self.response_class(**response_kwargs)

    def closed(self):
        if self.request.is_ajax():
            template_name = self.template_name_signup_closed_ajax
        else:
            template_name = self.template_name_signup_closed
        response_kwargs = {
            "request": self.request,
            "template": template_name,
        }
        return self.response_class(**response_kwargs)

class LoginView(FormView):

    template_name = "account/login.html"
    template_name_ajax = "account/ajax/login.html"
    form_class = LoginUsernameForm
    form_kwargs = {}
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(self.get_success_url())
        return super(LoginView, self).get(*args, **kwargs)

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.template_name_ajax]
        else:
            return [self.template_name]

    def get_context_data(self, **kwargs):
        ctx = super(LoginView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_form_kwargs(self):
        kwargs = super(LoginView, self).get_form_kwargs()
        kwargs.update(self.form_kwargs)
        return kwargs

    def form_invalid(self, form):
        signals.user_login_attempt.send(
            sender=LoginView,
            username=get_form_data(form, form.identifier_field),
            result=form.is_valid()
        )
        return super(LoginView, self).form_invalid(form)

    def form_valid(self, form):
        self.login_user(form)
        self.after_login(form)
        return redirect(self.get_success_url())

    def after_login(self, form):
        signals.user_logged_in.send(sender=LoginView, user=form.user, form=form)

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_LOGIN_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def login_user(self, form):
        auth.login(self.request, form.user)
        messages.success(self.request, 'You have successfully logged in.')
        expiry = settings.ACCOUNT_REMEMBER_ME_EXPIRY if form.cleaned_data.get("remember") else 0
        self.request.session.set_expiry(expiry)


class LogoutView(TemplateResponseMixin, View):

    template_name = "account/logout.html"
    redirect_field_name = "next"

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect(self.get_redirect_url())
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            messages.success(self.request, 'You have successfully logged out.')
            auth.logout(self.request)
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        ctx = kwargs
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_redirect_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_LOGOUT_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class ConfirmEmailView(TemplateResponseMixin, View):

    http_method_names = ["get", "post"]
    messages = {
        "email_confirmed": {
            "level": messages.SUCCESS,
            "text": _("You have confirmed {email}.")
        }
    }

    def get_template_names(self):
        return {
            "GET": ["account/email_confirm.html"],
            "POST": ["account/email_confirmed.html"],
        }[self.request.method]

    def get(self, *args, **kwargs):
        self.object = self.get_object()
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        confirmation.confirm()
        self.after_confirmation(confirmation)
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        if self.messages.get("email_confirmed"):
            messages.add_message(
                self.request,
                self.messages["email_confirmed"]["level"],
                self.messages["email_confirmed"]["text"].format(**{
                    "email": confirmation.email_address.email
                })
            )
        return redirect(redirect_url)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        try:
            return queryset.get(key=self.kwargs["key"].lower())
        except EmailConfirmation.DoesNotExist:
            raise Http404()

    def get_queryset(self):
        qs = EmailConfirmation.objects.all()
        qs = qs.select_related("email_address__user")
        return qs

    def get_context_data(self, **kwargs):
        ctx = kwargs
        ctx["confirmation"] = self.object
        return ctx

    def get_redirect_url(self):
        if self.request.user.is_authenticated():
            if not settings.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL:
                return settings.ACCOUNT_LOGIN_REDIRECT_URL
            return settings.ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL
        else:
            return settings.ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL

    def after_confirmation(self, confirmation):
        user = confirmation.email_address.user
        user.is_active = True
        user.save()


class ChangePasswordView(FormView):

    template_name = "account/password_change.html"
    form_class = ChangePasswordForm
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _("Password successfully changed.")
        }
    }

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return redirect("account_password_reset")
        return super(ChangePasswordView, self).get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return HttpResponseForbidden()
        return super(ChangePasswordView, self).post(*args, **kwargs)

    def change_password(self, form):
        user = self.request.user
        user.set_password(form.cleaned_data["password_new"])
        user.save()
        # required on Django >= 1.7 to keep the user authenticated
        if hasattr(auth, "update_session_auth_hash"):
            auth.update_session_auth_hash(self.request, user)

    def after_change_password(self):
        user = self.request.user
        signals.password_changed.send(sender=ChangePasswordView, user=user)
        if settings.ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE:
            self.send_email(user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = {"user": self.request.user, "initial": self.get_initial()}
        if self.request.method in ["POST", "PUT"]:
            kwargs.update({
                "data": self.request.POST,
                "files": self.request.FILES,
            })
        return kwargs

    def form_valid(self, form):
        self.change_password(form)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        ctx = super(ChangePasswordView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_PASSWORD_CHANGE_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def send_email(self, user):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        ctx = {
            "user": user,
            "protocol": protocol,
            "current_site": current_site,
        }
        hookset.send_password_change_email([user.email], ctx)


class PasswordResetView(FormView):

    template_name = "account/password_reset.html"
    template_name_sent = "account/password_reset_sent.html"
    form_class = PasswordResetForm
    token_generator = default_token_generator

    def get_context_data(self, **kwargs):
        context = super(PasswordResetView, self).get_context_data(**kwargs)
        context['THEME_CONTACT_EMAIL'] = settings.THEME_CONTACT_EMAIL
        if self.request.method == "POST" and "resend" in self.request.POST:
            context["resend"] = True
        return context

    def form_valid(self, form):
        self.send_email(form.cleaned_data["email"])
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_sent,
            "context": self.get_context_data(form=form)
        }
        return self.response_class(**response_kwargs)

    def send_email(self, email):
        User = get_user_model()
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        email_qs = EmailAddress.objects.filter(email__iexact=email)
        for user in User.objects.filter(pk__in=email_qs.values("user")):
            uid = int_to_base36(user.id)
            token = self.make_token(user)
            password_reset_url = "{0}://{1}{2}".format(
                protocol,
                current_site.domain,
                reverse("account_password_reset_token", kwargs=dict(uidb36=uid, token=token))
            )
            ctx = {
                "user": user,
                "current_site": current_site,
                "password_reset_url": password_reset_url,
            }
            hookset.send_password_reset_email([user.email], ctx)

    def make_token(self, user):
        return self.token_generator.make_token(user)


class PasswordResetTokenView(FormView):

    template_name = "account/password_reset_token.html"
    template_name_fail = "account/password_reset_token_fail.html"
    form_class = PasswordResetTokenForm
    token_generator = default_token_generator
    redirect_field_name = "next"
    messages = {
        "password_changed": {
            "level": messages.SUCCESS,
            "text": _("Password successfully changed.")
        },
    }

    def get(self, request, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        ctx = self.get_context_data(form=form)
        if not self.check_token(self.get_user(), self.kwargs["token"]):
            return self.token_fail()
        return self.render_to_response(ctx)

    def get_context_data(self, **kwargs):
        ctx = super(PasswordResetTokenView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "uidb36": self.kwargs["uidb36"],
            "token": self.kwargs["token"],
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def change_password(self, form):
        user = self.get_user()
        user.set_password(form.cleaned_data["password"])
        user.save()

    def after_change_password(self):
        user = self.get_user()
        signals.password_changed.send(sender=PasswordResetTokenView, user=user)
        if settings.ACCOUNT_NOTIFY_ON_PASSWORD_CHANGE:
            self.send_email(user)
        if self.messages.get("password_changed"):
            messages.add_message(
                self.request,
                self.messages["password_changed"]["level"],
                self.messages["password_changed"]["text"]
            )

    def form_valid(self, form):
        self.change_password(form)
        self.after_change_password()
        return redirect(self.get_success_url())

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_PASSWORD_RESET_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)

    def get_user(self):
        try:
            uid_int = base36_to_int(self.kwargs["uidb36"])
        except ValueError:
            raise Http404()
        return get_object_or_404(get_user_model(), id=uid_int)

    def check_token(self, user, token):
        return self.token_generator.check_token(user, token)

    def token_fail(self):
        response_kwargs = {
            "request": self.request,
            "template": self.template_name_fail,
            "context": self.get_context_data()
        }
        return self.response_class(**response_kwargs)

    def send_email(self, user):
        protocol = getattr(settings, "DEFAULT_HTTP_PROTOCOL", "http")
        current_site = get_current_site(self.request)
        ctx = {
            "user": user,
            "protocol": protocol,
            "current_site": current_site,
        }
        hookset.send_password_change_email([user.email], ctx)


class SettingsView(LoginRequiredMixin, FormView):

    template_name = "account/settings.html"
    form_class = SettingsForm
    redirect_field_name = "next"
    messages = {
        "settings_updated": {
            "level": messages.SUCCESS,
            "text": _("Account settings updated.")
        },
    }

    def get_form_class(self):
        # @@@ django: this is a workaround to not having a dedicated method
        # to initialize self with a request in a known good state (of course
        # this only works with a FormView)
        self.primary_email_address = EmailAddress.objects.get_primary(self.request.user)
        return super(SettingsView, self).get_form_class()

    def get_initial(self):
        initial = super(SettingsView, self).get_initial()
        if self.primary_email_address:
            initial["email"] = self.primary_email_address.email
        initial["timezone"] = self.request.user.account.timezone
        initial["language"] = self.request.user.account.language
        return initial

    def form_valid(self, form):
        self.update_settings(form)
        if self.messages.get("settings_updated"):
            messages.add_message(
                self.request,
                self.messages["settings_updated"]["level"],
                self.messages["settings_updated"]["text"]
            )
        return redirect(self.get_success_url())

    def update_settings(self, form):
        self.update_email(form)
        self.update_account(form)

    def update_email(self, form, confirm=None):
        user = self.request.user
        if confirm is None:
            confirm = settings.ACCOUNT_EMAIL_CONFIRMATION_EMAIL
        # @@@ handle multiple emails per user
        email = form.cleaned_data["email"].strip()
        if not self.primary_email_address:
            user.email = email
            EmailAddress.objects.add_email(self.request.user, email, primary=True, confirm=confirm)
            user.save()
        else:
            if email != self.primary_email_address.email:
                self.primary_email_address.change(email, confirm=confirm)

    def get_context_data(self, **kwargs):
        ctx = super(SettingsView, self).get_context_data(**kwargs)
        redirect_field_name = self.get_redirect_field_name()
        ctx.update({
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": self.request.POST.get(redirect_field_name, self.request.GET.get(redirect_field_name, "")),
        })
        return ctx

    def update_account(self, form):
        fields = {}
        if "timezone" in form.cleaned_data:
            fields["timezone"] = form.cleaned_data["timezone"]
        if "language" in form.cleaned_data:
            fields["language"] = form.cleaned_data["language"]
        if fields:
            account = self.request.user.account
            for k, v in fields.items():
                setattr(account, k, v)
            account.save()

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def get_success_url(self, fallback_url=None, **kwargs):
        if fallback_url is None:
            fallback_url = settings.ACCOUNT_SETTINGS_REDIRECT_URL
        kwargs.setdefault("redirect_field_name", self.get_redirect_field_name())
        return default_redirect(self.request, fallback_url, **kwargs)


class DeleteView(LogoutView):

    template_name = "account/delete.html"
    messages = {
        "account_deleted": {
            "level": messages.WARNING,
            "text": _("Your account is now inactive and your data will be expunged in the next {expunge_hours} hours.")
        },
    }

    def post(self, *args, **kwargs):
        AccountDeletion.mark(self.request.user)
        auth.logout(self.request)
        messages.add_message(
            self.request,
            self.messages["account_deleted"]["level"],
            self.messages["account_deleted"]["text"].format(**{
                "expunge_hours": settings.ACCOUNT_DELETION_EXPUNGE_HOURS,
            })
        )
        return redirect(self.get_redirect_url())

    def get_context_data(self, **kwargs):
        ctx = super(DeleteView, self).get_context_data(**kwargs)
        ctx.update(kwargs)
        ctx["ACCOUNT_DELETION_EXPUNGE_HOURS"] = settings.ACCOUNT_DELETION_EXPUNGE_HOURS
        return ctx
