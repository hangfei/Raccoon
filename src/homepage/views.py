from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render

def index(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/index.html', context)

def about_enverest(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'homepage/about_enverest.html', context)