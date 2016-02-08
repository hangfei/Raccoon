from django.shortcuts import render
from common.models import Client, Expert
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.template import RequestContext, loader
from django.core.exceptions import ObjectDoesNotExist

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