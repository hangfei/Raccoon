from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from common.models import Project
from common.models import Client
from common.models import Expert

from .forms import ProjectForm

state_message_option = {
    'ept_a':'The client will review it and get back to you',
    'clt_c':'We will review your project and an expert will be assigned to you soon',
}

def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('thanks?last_action=clt_c')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm(label_suffix=' ')

    return render(request, 'create.html', {'form': form})

def expertchoice(request):
    if request.method == 'GET':
      #TODO: sanity check
      if 'project_id' in request.GET:
        project_id_val = request.GET['project_id']
        project = Project.objects.get(pk=project_id_val)
        context = RequestContext(request, {
           'project': project,
        })
      return render(request, 'expertchoice.html', context)
    else:
      if 'project_id' in request.POST and 'accept_project' in request.POST:
        project_id_val = request.POST['project_id']
        project = Project.objects.get(pk=project_id_val)
        accept_val = request.POST['accept_project']
        if accept_val == 'A':
          project.state = 'ET'
        elif accept_val == 'D':
          project.state = 'PS'
        project.save()
      return HttpResponseRedirect('thanks?last_action=ept_a')


def clientchoice(request):
    return render(request, 'clientchoice.html', context)

def thanks(request):
    if 'last_action' in request.GET:
      message_val = request.GET['last_action']
      context = RequestContext(request, {
           'message_display': state_message_option[message_val],
      })
    return render(request, 'thanks.html', context)