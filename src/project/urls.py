from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create$', views.create, name='create'),
    url(r'^expertchoice$', views.expertchoice, name='expertchoice'),
    url(r'^expertstart$', views.expertstart, name='expertstart'),
    url(r'^expertworking$', views.expertworking, name='expertworking'),
    url(r'^clientchoice$', views.clientchoice, name='clientchoice'),
    url(r'^clientconfirm$', views.clientconfirm, name='clientconfirm'),
    url(r'^waitassignexpert$', views.waitassignexpert, name='waitassignexpert'),
    url(r'^waitclientconfirm$', views.waitclientconfirm, name='waitclientconfirm'),
    url(r'^waitexpertstart$', views.waitexpertstart, name='waitexpertstart'),
    url(r'^waitexpertworking$', views.waitexpertworking, name='waitexpertworking'),
    url(r'^waitpayment$', views.waitpayment, name='waitpayment'),
    url(r'^rateexpert$', views.rateexpert, name='rateexpert'),
    url(r'^close$', views.close, name='close'),
    url(r'^thanks$', views.thanks, name='thanks'),
    url(r'^unavailable$', views.unavailable, name='unavailable'),
    url(r'^clientonly$', views.clientonly, name='clientonly'),
]