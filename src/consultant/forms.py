
from django import forms
from django.forms import ModelForm
from common.models import project

class InvoiceUploadForm(ModelForm):

    class Meta:
        model = Project
        fields = ['invoice']

    # username = forms.CharField(
    #     label=_("Username"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=True
    # )
    # first_name = forms.CharField(
    #     label=_("Firstname"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=True
    # )
    # last_name = forms.CharField(
    #     label=_("Lastname"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=True
    # )
    # password = forms.CharField(
    #     label=_("Password"),
    #     widget=forms.PasswordInput(render_value=False)
    # )
    # password_confirm = forms.CharField(
    #     label=_("Password (again)"),
    #     widget=forms.PasswordInput(render_value=False)
    # )
    # email = forms.EmailField(
    #     label=_("Email"),
    #     widget=forms.TextInput(), required=True)

    # profile_image = forms.FileField(
    #     label='Select a image for your profile.',
    #     required=False
    # )

    # work_phone_number = forms.RegexField(
    #     regex=r'^\+?1?\d{9,15}$',
    #     error_messages = {
    #         'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
    #     },
    #     required=False
    # )

    # cell_phone_number = forms.RegexField(
    #     regex=r'^\+?1?\d{9,15}$',
    #     error_messages = {
    #         'invalid': ("Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."),
    #     },
    #     required=False
    # )

    # title = forms.CharField(
    #     label=_("Title"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=False
    # )
    # company = forms.CharField(
    #     label=_("Company"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=False
    # )

    # country = forms.CharField(
    #     label=_("Country"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=False
    # )

    # state = forms.CharField(
    #     label=_("State"),
    #     max_length=30,
    #     widget=forms.TextInput(),
    #     required=False
    # )

    # city = forms.CharField(
    #     label=_("City"),
    #     max_length=64,
    #     widget=forms.TextInput(),
    #     required=False
    # )

    # street = forms.CharField(
    #     label=_("Street Address"),
    #     max_length=128,
    #     widget=forms.TextInput(),
    #     required=False
    # )

    # zip_code = forms.CharField(
    #     label=_("Zip code"),
    #     max_length=10,
    #     widget=forms.TextInput(),
    #     required=False
    # )

    # terms = forms.BooleanField(
    #     error_messages={'required': 'You must accept the terms and conditions'},
    #     label=mark_safe('Agree to the Terms&Conditions (<a href="/terms_of_service" target="_blank">Read terms of service</a>)'),
    #     required=True
    # )

    # code = forms.CharField(
    #     max_length=64,
    #     required=False,
    #     widget=forms.HiddenInput()
    # )

    # def clean_username(self):
    #     if not alnum_re.search(self.cleaned_data["username"]):
    #         raise forms.ValidationError(_("Usernames can only contain letters, numbers and underscores."))
    #     User = get_user_model()
    #     lookup_kwargs = get_user_lookup_kwargs({
    #         "{username}__iexact": self.cleaned_data["username"]
    #     })
    #     qs = User.objects.filter(**lookup_kwargs)
    #     if not qs.exists():
    #         return self.cleaned_data["username"]
    #     raise forms.ValidationError(_("This username is already taken. Please choose another."))

    # def clean_email(self):
    #     value = self.cleaned_data["email"]
    #     qs = EmailAddress.objects.filter(email__iexact=value)
    #     if not qs.exists() or not settings.ACCOUNT_EMAIL_UNIQUE:
    #         return value
    #     raise forms.ValidationError(_("A user is registered with this email address."))

    # def clean(self):
    #     if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
    #         if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
    #             raise forms.ValidationError(_("You must type the same password each time."))
    #     return self.cleaned_data
