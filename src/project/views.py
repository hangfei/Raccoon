from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from common.models import Project,Client,Expert,CommentForExpert,CommentForClient

from .forms import ProjectForm
import logging

logger = logging.getLogger(__name__)

state_message_option = {
    'ept_a':'The client will review it and get back to you',
    'ept_f':'The client will review your work and get back to you',
    'ept_s':'Thank you for working on this project and the client will be notified soon',
    'clt_s':'We will review your project and an expert will be assigned to you soon',
    'clt_c':'You will receive the contract and payment information soon',
    'clt_n':'The expert will keep working on the project',
    'clt_y':'The project is now finished',
    'clt_a':'An administrator will contact you soon',
    'rating':'Your rating will help us improve',
}

def getCurrentRole(request):
    User = get_user_model()
    if request.user.id == None:
      return False
    user_id = request.user.id
    profile_user = User.objects.get(pk=user_id)
    user_profiles = profile_user.userprofile_set.all()
    user_profile = None
    if user_profiles:
        user_profile = user_profiles[0]
    else:
        return None
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
    return person

def hasPermission(request, project, require_expert):
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
        if require_expert == True:
          return False
        clients = profile_user.client_set.all()
        person = clients[0]
        if person != project.client:
            return False
    elif user_profile.user_type == 'EXPERT':
        if require_expert == False:
          return False
        experts = profile_user.expert_set.all()
        person = experts[0]
        if person != project.expert:
            return False
    else:
        return False
    #    raise ObjectDoesNotExist("user doesn't assoicate with any client/expert.")
    return True

#Check if the current role in the request: 
#client return True, expert return False; no such user return None
def isClient(request):
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
        return None
    if user_profile.user_type == 'CLIENT':
      return True
    return False

#This is the utility function for post method, it checks the permission and
#if it has the permission it will get the project from the db and return,
#Otherwise it will return None
def getProjectFromPost(request, expectStatus, require_expert):
    if request.method != 'POST':
      return None
    if 'project_id' not in request.POST:
      return None
    project_id_val = request.POST['project_id']
    project = None
    try:
      project = Project.objects.get(pk=project_id_val)
    except ObjectDoesNotExist:
      return None
    if(project.state not in expectStatus):
      return None
    if hasPermission(request, project, require_expert) == False:
      return None
    return project

def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        if isClient(request) == False:
          return HttpResponseRedirect('clientonly')
        # create a form instance and populate it with data from the request:
        form = ProjectForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            new_project = Project(client=getCurrentRole(request),
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
        result = isClient(request)
        if result == False or result ==None:
          return HttpResponseRedirect('clientonly')
        form = ProjectForm(label_suffix=' ')

    return render(request, 'create.html', {'form': form})

def expertchoice(request):
    if request.method == 'GET':
        logger.info("expertchoice GET")
        return generalGetPage(request, 'expertchoice', set(['EA']), True)
    else:
      project = getProjectFromPost(request, set(['EA']), True)
      if project == None:
        return HttpResponseRedirect('unavailable')
      if 'accept_project' not in request.POST:
        return HttpResponseRedirect('unavailable')
      accept_val = request.POST['accept_project']
      if accept_val == 'A':
        project.state = 'ET'
      elif accept_val == 'D':
        project.state = 'PS'
      project.save()
      return HttpResponseRedirect('thanks?last_action=ept_a')


def clientchoice(request):
    if request.method == 'GET':
        return generalGetPage(request, 'clientchoice', set(['ET']), False)
    else:
      project = getProjectFromPost(request, set(['ET']), False)
      if project == None:
        return HttpResponseRedirect('unavailable')
      if 'accept_expert' not in request.POST:
        return HttpResponseRedirect('unavailable')
      accept_val = request.POST['accept_expert']
      if accept_val == 'A':
        project.state = 'CA'
      elif accept_val == 'D':
        project.state = 'PS'
      project.save()
      return HttpResponseRedirect('thanks?last_action=clt_c')

def expertworking(request):
    if request.method == 'GET':
      return generalGetPage(request, 'expertworking', set(['IP']), True)
    else:
      project = getProjectFromPost(request, set(['IP']), True)
      if project == None:
        return HttpResponseRedirect('unavailable')
      project.state = 'PF'
      project.save()
      return HttpResponseRedirect('thanks?last_action=ept_f')

def expertstart(request):
    if request.method == 'GET':
      return generalGetPage(request, 'expertstart', set(['CA']), True)
    else:
      project = getProjectFromPost(request, set(['CA']), True)
      if project == None:
        return HttpResponseRedirect('unavailable')
      project.state = 'IP'
      project.save()
      return HttpResponseRedirect('thanks?last_action=ept_s')

def clientconfirm(request):
    if request.method == 'GET':
      return generalGetPage(request, 'clientconfirm', set(['PF']), False)
    else:
      project = getProjectFromPost(request, set(['PF']), False)
      if project == None:
        return HttpResponseRedirect('unavailable')
      if 'accept_finish' not in request.POST:
        return HttpResponseRedirect('unavailable')
      redirectStr = ''
      confirm_val = request.POST['accept_finish']
      if confirm_val == 'Y': #Accept finish
        project.state = 'CC'
        project.save()
        return HttpResponseRedirect('rate?project_id='+str(project.pk))
      elif confirm_val == 'N': #Need more work
        project.state = 'IP'
        redirectStr = 'clt_n'
      elif confirm_val == 'A': #Cannot make agreement, Appeal
        project.state = 'AD'
        redirectStr = 'clt_a'
      project.save()
      return HttpResponseRedirect('thanks?last_action='+redirectStr)

def waitassignexpert(request):
    return generalGetPage(request, 'waitassignexpert', set(['PS','EA']), False)

def waitclientconfirm(request):
    return generalGetPage(request, 'waitclientconfirm', set(['PF','ET']), True)

def waitexpertstart(request):
    return generalGetPage(request, 'waitexpertstart', set(['CA']), False)

def waitexpertworking(request):
    return generalGetPage(request, 'waitexpertworking',set(['IP']), False)

def waitpayment(request):
    return generalGetPage(request, 'waitpayment',set(['CC']), True)

def rate(request):
  if request.method == 'GET':
    return generalGetPage(request, 'rate',set(['CC','PF']), None)
  else:
    cur_project = getProjectFromPost(request, set(['CC','PF']), None)
    if cur_project == None:
        return HttpResponseRedirect('unavailable')
    if 'comment' not in request.POST or 'rating' not in request.POST:
        return HttpResponseRedirect('unavailable')
    comment_text = request.POST['comment']
    rating = request.POST['rating']
    if isClient(request):
        new_comment = CommentForExpert(project=cur_project,
                                       expert=cur_project.expert,
                                       text=comment_text,
                                       rating=float(rating)
                                       )
        new_comment.save()

        #Update the expert rating by calculating the weighted rating
        cur_expert = cur_project.expert
        cur_expert.rating = (float((cur_expert.rating)*(cur_expert.comments_num))+float(rating))/(cur_expert.comments_num+1)
        cur_expert.comments_num += 1
        cur_expert.save()
    else:
        new_comment = CommentForClient(project=cur_project,
                                       client=cur_project.client,
                                       text=comment_text,
                                       rating=float(rating)
                                       )
        new_comment.save()

        #Update the client rating by calculating the weighted rating
        cur_client = cur_project.client
        cur_client.rating = (float((cur_client.rating)*(cur_client.comments_num))+float(rating))/(cur_client.comments_num+1)
        cur_client.comments_num += 1
        cur_client.save()
    return HttpResponseRedirect('thanks?last_action=rating')

def close(request):
    return generalGetPage(request, 'close',set(['PR','CC']), None)

def generalGetPage(request, pageStatus, expectStatus, require_expert):
    if request.method == 'GET':
        if 'project_id' in request.GET:
            project_id_val = request.GET['project_id']
            project = None
            try:
                project = Project.objects.get(pk=project_id_val)
            except ObjectDoesNotExist:
                return HttpResponseRedirect('unavailable')
            if(project.state not in expectStatus):
                return HttpResponseRedirect('unavailable')
            if hasPermission(request, project, require_expert) == False:
                return HttpResponseRedirect('unavailable')
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

def clientonly(request):
    return render(request, 'clientonly.html')