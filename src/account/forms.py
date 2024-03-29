from __future__ import unicode_literals

import re

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = None

from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from django.contrib import auth
from django.contrib.auth import get_user_model
from django.utils.safestring import mark_safe
from account.conf import settings
from account.hooks import hookset
from common.models import EmailAddress
from common.models import Expert
from common.multichoice import MultiSelectFormField
from account.utils import get_user_lookup_kwargs


alnum_re = re.compile(r"^\w+$")

from django.core.validators import RegexValidator


class ConsultantSignupForm(ModelForm):

    class Meta:
        model = Expert
        fields = ['description_text', 'area', 'industries', 'expertise', 'experience', 'education']
        widgets = {
          'description_text':forms.Textarea(
                                        attrs={'placeholder':_('Introduce yourself to the potential clients'),
                                                'rows':10,
                                                'cols':39}),
           'industries':forms.CheckboxSelectMultiple
        }


    username = forms.CharField(
        label=_("Username *"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    first_name = forms.CharField(
        label=_("Firstname *"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    last_name = forms.CharField(
        label=_("Lastname *"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    password = forms.CharField(
        label=_("Password *"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again) *"),
        widget=forms.PasswordInput(render_value=False)
    )
    email = forms.EmailField(
        label=_("Email *"),
        widget=forms.TextInput(), required=True)

    profile_image = forms.FileField(
        label=_('Select a image for your profile.'),
        required=False
    )

    work_phone_number = forms.RegexField(
        label=_("Work phone number"),
        regex=r'^\+?1?\d{9,15}$',
        error_messages = {
            'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        },
        required=False
    )

    cell_phone_number = forms.RegexField(
        label=_("Cell phone number"),
        regex=r'^\+?1?\d{9,15}$',
        error_messages = {
            'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        },
        required=False
    )

    title = forms.CharField(
        label=_("Title"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )
    company = forms.CharField(
        label=_("Company"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    country = forms.CharField(
        label=_("Country"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    state = forms.CharField(
        label=_("State"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    city = forms.CharField(
        label=_("City"),
        max_length=64,
        widget=forms.TextInput(),
        required=False
    )

    street = forms.CharField(
        label=_("Street Address"),
        max_length=128,
        widget=forms.TextInput(),
        required=False
    )

    zip_code = forms.CharField(
        label=_("Zip code"),
        max_length=10,
        widget=forms.TextInput(),
        required=False
    )

    terms = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
        label=mark_safe('Agree to the Terms&Conditions (<a href="/terms_of_service" target="_blank">Read terms of service</a>)'),
        required=True
    )

    code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )
    
    def __init__(self, *args, **kwargs):
        super(ConsultantSignupForm, self).__init__(*args, **kwargs)
        self.fields['description_text'].label = _("Description *")
        self.fields['area'].label = _("Area *")
        self.fields['industries'].label = _("Industries *")
        self.fields['experience'].label = _("Experience *")
        self.fields['expertise'].label = _("Expertise *")
        self.fields['education'].label = _("Education *")
        
    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data


class ClientSignupForm(forms.Form):

    username = forms.CharField(
        label=_("Username *"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    first_name = forms.CharField(
        label=_("Firstname *"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    last_name = forms.CharField(
        label=_("Lastname *"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    password = forms.CharField(
        label=_("Password *"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("Password (again) *"),
        widget=forms.PasswordInput(render_value=False)
    )
    email = forms.EmailField(
        label=_("Email *"),
        widget=forms.TextInput(), required=True)

    profile_image = forms.FileField(
        label=_('Select a image for your profile.'),
        required=False
    )

    work_phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_messages = {
            'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        },
        required=False
    )
    cell_phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_messages = {
            'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        },
        required=False
    )

    title = forms.CharField(
        label=_("Title"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )
    company = forms.CharField(
        label=_("Company"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    country = forms.CharField(
        label=_("Country"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    state = forms.CharField(
        label=_("State"),
        max_length=30,
        widget=forms.TextInput(),
        required=False
    )

    city = forms.CharField(
        label=_("City"),
        max_length=64,
        widget=forms.TextInput(),
        required=False
    )

    street = forms.CharField(
        label=_("Street Address"),
        max_length=128,
        widget=forms.TextInput(),
        required=False
    )

    zip_code = forms.CharField(
        label=_("Zip code"),
        max_length=10,
        widget=forms.TextInput(),
        required=False
    )

    terms = forms.BooleanField(
        error_messages={'required': 'You must accept the terms and conditions'},
        label=mark_safe('Agree to the Terms&Conditions (<a href="/terms_of_service" target="_blank">Read terms of service</a>)'),
        required=True
    )

    code = forms.CharField(
        max_length=64,
        required=False,
        widget=forms.HiddenInput()
    )

    def clean_username(self):
        if not alnum_re.search(self.cleaned_data["username"]):
            raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
        User = get_user_model()
        lookup_kwargs = get_user_lookup_kwargs({
            "{username}__iexact": self.cleaned_data["username"]
        })
        qs = User.objects.filter(**lookup_kwargs)
        if not qs.exists():
            return self.cleaned_data["username"]
        raise forms.ValidationError(_("This username is already taken. Please choose another."))

    def clean_email(self):
        value = self.cleaned_data["email"]
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))

    def clean(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data


class LoginForm(forms.Form):

    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False
    )
    user = None

    def clean(self):
        if self._errors:
            return
        user = auth.authenticate(**self.user_credentials())
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is inactive."))
        else:
            raise forms.ValidationError(self.authentication_fail_message)
        return self.cleaned_data

    def user_credentials(self):
        return hookset.get_user_credentials(self, self.identifier_field)


class LoginUsernameForm(LoginForm):

    username = forms.CharField(label=_("Username"), max_length=30)
    authentication_fail_message = _("The username and/or password you specified are not correct.")
    identifier_field = "username"

    def __init__(self, *args, **kwargs):
        super(LoginUsernameForm, self).__init__(*args, **kwargs)
        field_order = ["username", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class LoginEmailForm(LoginForm):

    email = forms.EmailField(label=_("Email"))
    authentication_fail_message = _("The email address and/or password you specified are not correct.")
    identifier_field = "email"

    def __init__(self, *args, **kwargs):
        super(LoginEmailForm, self).__init__(*args, **kwargs)
        field_order = ["email", "password", "remember"]
        if not OrderedDict or hasattr(self.fields, "keyOrder"):
            self.fields.keyOrder = field_order
        else:
            self.fields = OrderedDict((k, self.fields[k]) for k in field_order)


class ChangePasswordForm(forms.Form):

    password_current = forms.CharField(
        label=_("Current Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_new_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_password_current(self):
        if not self.user.check_password(self.cleaned_data.get("password_current")):
            raise forms.ValidationError(_("Please type your current password."))
        return self.cleaned_data["password_current"]

    def clean_password_new_confirm(self):
        if "password_new" in self.cleaned_data and "password_new_confirm" in self.cleaned_data:
            if self.cleaned_data["password_new"] != self.cleaned_data["password_new_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_new_confirm"]


class PasswordResetForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)

    def clean_email(self):
        value = self.cleaned_data["email"]
        if not EmailAddress.objects.filter(email__iexact=value).exists():
            raise forms.ValidationError(_("Email address can not be found."))
        return value


class PasswordResetTokenForm(forms.Form):

    password = forms.CharField(
        label=_("New Password"),
        widget=forms.PasswordInput(render_value=False)
    )
    password_confirm = forms.CharField(
        label=_("New Password (again)"),
        widget=forms.PasswordInput(render_value=False)
    )

    def clean_password_confirm(self):
        if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
            if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
                raise forms.ValidationError(_("You must type the same password each time."))
        return self.cleaned_data["password_confirm"]


class SettingsForm(forms.Form):

    email = forms.EmailField(label=_("Email"), required=True)
    timezone = forms.ChoiceField(
        label=_("Timezone"),
        choices=[("", "---------")] + settings.ACCOUNT_TIMEZONES,
        required=False
    )
    if settings.USE_I18N:
        language = forms.ChoiceField(
            label=_("Language"),
            choices=settings.ACCOUNT_LANGUAGES,
            required=False
        )

    def clean_email(self):
        value = self.cleaned_data["email"]
        if self.initial.get("email") == value:
            return value
        qs = EmailAddress.objects.filter(email__iexact=value)
        if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
            return value
        raise forms.ValidationError(_("A user is registered with this email address."))
