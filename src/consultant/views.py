from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from common.models import Project
from common.models import Client
from common.models import Expert

def dashboard(request):
	test = "Shiming"
	project_list = Project.objects.filter(client__user__first_name=test)
	context = { 'project_list': project_list }
	return render(request, 'consultant/dashboard.html', context)