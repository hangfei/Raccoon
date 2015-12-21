from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from .models import Project
from .models import Client
from .models import Expert

def index(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'consultants/index.html', context)

def dashboard(request):
	test = 'Shiming'
	project_list = Project.objects.filter(client__first_name_text=test)
	context = { 'project_list': project_list }
	return render(request, 'consultants/dashboard.html', context)