from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from common.models import Project, Client, Expert, UserProfile
from django.contrib.auth import get_user_model

def getUser(request):
    User = get_user_model()
    if request.user.id == None:
      return None
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)
    user_profiles = profile_user.userprofile_set.all()
    #
    user_profile = None
    if user_profiles:
        user_profile = user_profiles[0]
    else:
    #   raise ObjectDoesNotExist("user doesn't assoicate with any user_profile.")
         return None
    person = None
    is_expert = None

    if user_profile.user_type == 'CLIENT':
        is_expert = False
        clients = profile_user.client_set.all()
        person = clients[0]
        return person
    elif user_profile.user_type == 'EXPERT':
        is_expert = True
        experts = profile_user.expert_set.all()
        person = experts[0]
        return person
    #    raise ObjectDoesNotExist("user doesn't assoicate with any client/expert.")
    return None

def dashboard(request):
    person = getUser(request)
    if type(person) == Expert:
        project_list = Project.objects.filter(expert=person)
        context = { 'project_list': project_list }
        return render(request, 'consultant/expert_dashboard.html', context)
    elif type(person) == Client:
        project_list = Project.objects.filter(client=person)
        user = request.user
        experts = set()
        if user.is_authenticated():
            user_profiles = UserProfile.objects.filter(user=user)
            if user_profiles:
                user_profile = user_profiles[0]
                if user_profile.user_type == 'CLIENT':
                    client = Client.objects.filter(user=user)[0]
                    experts = set([project.expert for project in Project.objects.filter(client=client)])

        context = { 'project_list': project_list,
                    'experts': experts
                  }
        return render(request, 'consultant/client_dashboard.html', context)