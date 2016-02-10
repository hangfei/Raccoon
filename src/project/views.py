from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from common.models import Project
from common.models import Client
from common.models import Expert

from .forms import ProjectForm

state_message_option = {
    'ept_a':'The client will review it and get back to you',
    'ept_f':'The client will review your work and get back to you',
    'ept_s':'Thank you for working on this project and the client will be notified soon',
    'clt_s':'We will review your project and an expert will be assigned to you soon',
    'clt_c':'You will receive the contract and payment information soon',
    'clt_n':'The expert will keep working on the project',
    'clt_y':'The project is now finished',
    'clt_a':'An administrator will contact you soon',
}

def hasPermission(request, project):
    print("user::")
    print(request.user)
    User = get_user_model()
    if request.user.id == None or project == None:
      return False
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)
    user_profiles = profile_user.userprofile_set.all()
    #
    user_profile = None
    if user_profiles:
        user_profile = user_profiles[0]
    else:
    #   raise ObjectDoesNotExist("user doesn't assoicate with any user_profile.")
         return False
    person = None
    is_expert = None

    if user_profile.user_type == 'CLIENT':
        is_expert = False
        clients = profile_user.client_set.all()
        person = clients[0]
        print(person)
        print(project.client)
        if person != project.client:
            return False
    elif user_profile.user_type == 'EXPERT':
        is_expert = True
        experts = profile_user.expert_set.all()
        person = experts[0]
        print(person)
        print(project.client)
        if person != project.expert:
            return False
    else:
        return False
    #    raise ObjectDoesNotExist("user doesn't assoicate with any client/expert.")
    return True

def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(form.cleaned_data['project_name'])
            print(form.cleaned_data['project_expert_expertise'])
            new_project = Project(client=(Client.objects.all())[0],#getCurrentRole(request),
                                  expert=(Expert.objects.all())[0],
                                  title_text=form.cleaned_data['project_name'],
                                  info_text=form.cleaned_data['project_description'],
                                  expert_pref_text=form.cleaned_data['project_expert_preference'],
                                  pub_date=form.cleaned_data['project_pub_date'],
                                  end_date=form.cleaned_data['project_end_date'],
                                  rate=form.cleaned_data['project_rate'],
                                  assign_history='',
                                  state='PS',
                                  assgin_to='ADM',
                                  industry=form.cleaned_data['project_expert_industry'],
                                  expertise=form.cleaned_data['project_expert_expertise'],
                                  rate_type=form.cleaned_data['project_rate_type'],
                                  service_type=form.cleaned_data['project_service_type'],
                )
            new_project.save()
            # redirect to a new URL:
            return HttpResponseRedirect('thanks?last_action=clt_s')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ProjectForm(label_suffix=' ')

    return render(request, 'create.html', {'form': form})

def expertchoice(request):
    if request.method == 'GET':
       if 'project_id' in request.GET:
         project_id_val = request.GET['project_id']
         project = None
         try:
            project = Project.objects.get(pk=project_id_val)
         except ObjectDoesNotExist:
            return HttpResponseRedirect('unavailable')
         if hasPermission(request, project) == False:
            return HttpResponseRedirect('unavailable')
         context = RequestContext(request, {
           'project': project,
          })
         return render(request, 'expertchoice.html', context)
       return HttpResponseRedirect('unavailable') 
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
    if request.method == 'GET':
      #TODO: sanity check
      if 'project_id' in request.GET:
        project_id_val = request.GET['project_id']
        project = Project.objects.get(pk=project_id_val)
        context = RequestContext(request, {
           'project': project,
        })
      return render(request, 'clientchoice.html', context)
    else:
      if 'project_id' in request.POST and 'accept_expert' in request.POST:
        project_id_val = request.POST['project_id']
        project = Project.objects.get(pk=project_id_val)
        accept_val = request.POST['accept_expert']
        if accept_val == 'A':
          project.state = 'CA'
        elif accept_val == 'D':
          project.state = 'PS'
        project.save()
      return HttpResponseRedirect('thanks?last_action=clt_c')

def expertworking(request):
    if request.method == 'GET':
      #TODO: sanity check
      if 'project_id' in request.GET:
        project_id_val = request.GET['project_id']
        project = Project.objects.get(pk=project_id_val)
        context = RequestContext(request, {
           'project': project,
        })
      return render(request, 'expertworking.html', context)
    else:
      if 'project_id' in request.POST:
        project_id_val = request.POST['project_id']
        project = Project.objects.get(pk=project_id_val)
        project.state = 'PF'
        project.save()
      return HttpResponseRedirect('thanks?last_action=ept_f')

def expertstart(request):
    if request.method == 'GET':
      return generalGetPage(request, 'expertstart')
    else:
      if 'project_id' in request.POST:
        project_id_val = request.POST['project_id']
        project = Project.objects.get(pk=project_id_val)
        project.state = 'IP'
        project.save()
      return HttpResponseRedirect('thanks?last_action=ept_s')

def clientconfirm(request):
    if request.method == 'GET':
      #TODO: sanity check
      if 'project_id' in request.GET:
        project_id_val = request.GET['project_id']
        project = Project.objects.get(pk=project_id_val)
        context = RequestContext(request, {
           'project': project,
        })
      return render(request, 'clientconfirm.html', context)
    else:
      redirectStr = ''
      if 'project_id' in request.POST and 'accept_finish' in request.POST:
        project_id_val = request.POST['project_id']
        project = Project.objects.get(pk=project_id_val)
        confirm_val = request.POST['accept_finish']
        if confirm_val == 'Y': #Accept finish
          project.state = 'CC'
          redirectStr = 'clt_y'
        elif confirm_val == 'N': #Need more work
          project.state = 'IP'
          redirectStr = 'clt_n'
        elif confirm_val == 'A': #Cannot make agreement, Appeal
          project.state = 'AD'
          redirectStr = 'clt_a'
        project.save()
      return HttpResponseRedirect('thanks?last_action='+redirectStr)

def waitassignexpert(request):
    return generalGetPage(request, 'waitassignexpert')

def waitclientconfirm(request):
    return generalGetPage(request, 'waitclientconfirm')

def waitexpertstart(request):
    return generalGetPage(request, 'waitexpertstart')

def waitexpertworking(request):
    return generalGetPage(request, 'waitexpertworking')

def waitpayment(request):
    return generalGetPage(request, 'waitpayment')

def close(request):
    return generalGetPage(request, 'close')

def generalGetPage(request, pageStatus):
    if request.method == 'GET':
        if 'project_id' in request.GET:
            project_id_val = request.GET['project_id']
            project = None
            try:
                project = Project.objects.get(pk=project_id_val)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('unavailable')
            #if hasPermission(request, project) == False:
            #    return HttpResponseRedirect('unavailable')
            context = RequestContext(request, {
               'project': project,
              })
            return render(request, pageStatus+'.html', context)
        return HttpResponseRedirect('unavailable')

def thanks(request):
    if 'last_action' in request.GET:
      message_val = request.GET['last_action']
      context = RequestContext(request, {
           'message_display': state_message_option[message_val],
      })
    return render(request, 'thanks.html', context)

def unavailable(request):
    return render(request, 'unavailable.html')