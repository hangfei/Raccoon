from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from common.models import Expert, UserProfile, Client, Project

class ExpertDetailView(DetailView):

    model = Expert

    def get_context_data(self, **kwargs):
        context = super(ExpertDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ExpertListView(ListView):

    model = Expert
    paginate_by = 10
    context_object_name = "expert_list"

    def get_queryset(self):
        return_set = Expert.objects.all()
        if self.request.method == 'GET' and 'industry' in self.request.GET:
            industry_val = self.request.GET['industry']
            if industry_val != 'ALL':
              return_set = return_set.filter(industries__icontains=industry_val)
        if self.request.method == 'GET' and 'expertise' in self.request.GET:
            expertise_val = self.request.GET['expertise']
            if expertise_val != 'ALL':
              return_set = return_set.filter(expertise__icontains=expertise_val)
        if self.request.method == 'GET' and 'experience' in self.request.GET:
            experience_val = self.request.GET['experience']
            if experience_val != 'ALL':
              return_set = return_set.filter(experience=experience_val)
        if self.request.method == 'GET' and 'area' in self.request.GET:
            area_val = self.request.GET['area']
            if area_val != 'ALL':
              return_set = return_set.filter(area=area_val)
        return return_set

    def get_context_data(self, **kwargs):
        context = super(ExpertListView, self).get_context_data(**kwargs)
        # TODO this is not efficient. Need to optimize.
        can_views = []
        user = self.request.user
        if self.request.user.is_authenticated():
            user_profiles = UserProfile.objects.filter(user=user)
            if user_profiles:
                user_profile = user_profiles[0]
                if user_profile.user_type == 'CLIENT':
                    client = Client.objects.filter(user=user)[0]
                    can_views = [project.expert.id for project in Project.objects.filter(client=client)]
        context['now'] = timezone.now()
        context['can_views'] = can_views
        return context

#def filter(request):

#def index(request):
#    context = RequestContext(request, {
#        'latest_question_list': 'sss',
#    })
#    return render(request, 'consultants/index.html', context)