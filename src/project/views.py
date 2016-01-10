from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect
from common.models import Project
from common.models import Client
from common.models import Expert

from .forms import ProjectForm

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
            return HttpResponseRedirect('thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm(label_suffix=' ')

    return render(request, 'create.html', {'form': form})