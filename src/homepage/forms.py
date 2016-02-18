from __future__ import unicode_literals

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

class JoinUsForm(forms.Form):

    first_name = forms.CharField(
        label=_("Firstname"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    last_name = forms.CharField(
        label=_("Lastname"),
        max_length=30,
        widget=forms.TextInput(),
        required=True
    )
    email = forms.EmailField(
        label=_("Email"),
        widget=forms.TextInput(), required=True
    )
    phone_number = forms.RegexField(
        regex=r'^\+?1?\d{9,15}$',
        error_messages = {
            'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
        },
        required=False
    )
    tell_us_more = forms.CharField(
        label=_("Tell Us More"),
        max_length=1000,
        widget=forms.Textarea(attrs={'rows': 5}),
        required=True
    )