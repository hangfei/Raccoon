from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin
from django.utils import timezone

from common.models import Expert

class ExpertDetailView(DetailView):

    model = Expert
    
    def get_context_data(self, **kwargs):
        context = super(ExpertDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ExpertListView(ListView):

    model = Expert
    paginate_by = 5
    context_object_name = "expert_list"

    def get_queryset(self):
        return_set = Expert.objects.all()
        if self.request.method == 'GET' and 'level' in self.request.GET:
            level = self.request.GET['level']
            if level != 'ALL':
              return_set = return_set.filter(status=level)
        if self.request.method == 'GET' and 'area' in self.request.GET:
            city = self.request.GET['area']
            if city != 'ALL':
              return_set = return_set.filter(area=city)
        return return_set

    def get_context_data(self, **kwargs):
        context = super(ExpertListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

#def filter(request):

#def index(request):
#    context = RequestContext(request, {
#        'latest_question_list': 'sss',
#    })
#    return render(request, 'consultants/index.html', context)