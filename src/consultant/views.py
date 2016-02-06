from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from common.models import Project
from common.models import Client
from common.models import Expert
from django.contrib.auth import get_user_model

def getUser(request):
    print("user::")
    print(request.user)
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
	elif type(person) == Client:
	  project_list = Project.objects.filter(client=person)
	  context = { 'project_list': project_list }	
	return render(request, 'consultant/dashboard.html', context)