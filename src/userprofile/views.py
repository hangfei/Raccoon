from django.shortcuts import render
from common.models import Client, Expert, UserProfile
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist


from django.views.generic.edit import UpdateView
from django.forms import ModelForm
from django import forms
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

class ConsultantSignupForm(ModelForm):
    class Meta:
        model = Expert
        fields = ['description_text', 'status', 'area', 'industry', 'expertise', 'experience']


class ClientSignupForm(ModelForm):
    class Meta:
        model = Client
        fields = []

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

# https://collingrady.wordpress.com/2008/02/18/editing-multiple-objects-in-django-with-newforms/
def userprofile_edit(request):
    User = get_user_model()
    profile_user = User.objects.get(username=request.user)
    user_profiles = profile_user.userprofile_set.all()
    user_profile = None
    if user_profiles:
        user_profile = user_profiles[0]
    else:
        raise ObjectDoesNotExist("user doesn't assoicate with any user_profile.")
    person = None
    is_expert = None

    if user_profile.user_type == 'CLIENT':
        is_expert = False
        clients = profile_user.client_set.all()
        person = clients[0]
    elif user_profile.user_type == 'EXPERT':
        is_expert = True
        experts = profile_user.expert_set.all()
        person = experts[0]
    else:
        raise ObjectDoesNotExist("user doesn't assoicate with any client/expert.")


    if request.method == "POST":
        pform = None
        if is_expert:
            pform = ConsultantSignupForm(request.POST, instance=person)
        else:
            pform = ClientSignupForm(request.POST, instance=person)
        if pform.is_valid():
            pform.save()
            return HttpResponseRedirect('/profile/' + str(profile_user.username))
    else:
        pform = None
        if is_expert:
            pform = ConsultantSignupForm(instance=person)
        else:
            pform = ClientSignupForm(instance=person)
    return render(request, 'userprofile/update_userprofile.html', {'form': pform})



def user_profile(request, username):
    User = get_user_model()
    profile_user = User.objects.get(username=username)
    user_profiles = profile_user.userprofile_set.all()
    user_profile = None
    if user_profiles:
        user_profile = user_profiles[0]
    else:
        raise ObjectDoesNotExist("user doesn't assoicate with any user_profile.")
    person = None
    is_expert = None

    if user_profile.user_type == 'CLIENT':
        is_expert = False
        clients = profile_user.client_set.all()
        person = clients[0]
    elif user_profile.user_type == 'EXPERT':
        is_expert = True
        experts = profile_user.expert_set.all()
        person = experts[0]
    else:
        raise ObjectDoesNotExist("user doesn't assoicate with any client/expert.")


    current_user = request.user
    current_user_profiles = current_user.userprofile_set.all()
    current_user_profile = None
    if current_user_profiles:
        current_user_profile = current_user_profiles[0]
    else:
        raise ObjectDoesNotExist("user doesn't assoicate with any user_profile.")

    current_person = None
    current_is_expert = None

    if current_user_profile.user_type == 'CLIENT':
        current_is_expert = False
        clients = current_user.client_set.all()
        current_person = clients[0]
    elif current_user_profile.user_type == 'EXPERT':
        current_is_expert = True
        experts = current_user.expert_set.all()
        current_person = experts[0]
    else:
        raise ObjectDoesNotExist("user doesn't assoicate with any client/expert.")

    can_view_personal_info = False
    if current_user == profile_user:
        can_view_personal_info = True
    elif not current_is_expert:
        can_view_personal_info = current_person.has_worked_before(person)


    context = RequestContext(request, {
        'person': person,
        'profile_user': profile_user,
        'is_expert': is_expert,
        'can_view_personal_info': can_view_personal_info
    })
    return render(request, 'userprofile/profile.html', context)