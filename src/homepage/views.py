from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

def index(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/index.html', context)

def about_us(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/about_us.html', context)

def service(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/service.html', context)

def how_it_works(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/how_it_works.html', context)

def member_benefits(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/member_benefits.html', context)

def team(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/team.html', context)

def news_blog(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/news_blog.html', context)

def contact_us(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/contact_us.html', context)

def terms_of_service(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/terms_of_service.html', context)

from django.contrib.auth.decorators import user_passes_test

# https://djangosnippets.org/snippets/1703/
def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in."""
    def in_groups(u):
        if u.is_authenticated():
            if bool(u.groups.filter(name__in=group_names)) | u.is_superuser:
                return True
        return False
    return user_passes_test(in_groups)

@group_required('client')
def client_see_this(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/client_see_this.html', context)

@group_required('expert')
def expert_see_this(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/expert_see_this.html', context)


