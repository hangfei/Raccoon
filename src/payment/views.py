from django.http import HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'payment/index.html', context)

@login_required
def bank_transfer(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'payment/bank_transfer.html', context)

@login_required
def bank_transfer_detail(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'payment/bank_transfer_detail.html', context)

@login_required
def bank_transfer_beijing(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'payment/bank_transfer_beijing.html', context)

@login_required
def alipay(request):
    context = RequestContext(request, {
        'latest_question_list': 'sss',
    })
    return render(request, 'payment/alipay.html', context)