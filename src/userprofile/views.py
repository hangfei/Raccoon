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
    context = RequestContext(request, {
        'person': person,
        'profile_user': profile_user,
        'is_expert': is_expert
    })
    return render(request, 'userprofile/profile.html', context)