from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^create$', views.create, name='create'),
    url(r'^expertchoice$', views.expertchoice, name='expertchoice'),
    url(r'^expertworking$', views.expertworking, name='expertworking'),
    url(r'^clientchoice$', views.clientchoice, name='clientchoice'),
    url(r'^clientconfirm$', views.clientconfirm, name='clientconfirm'),
    url(r'^thanks$', views.thanks, name='thanks'),
    url(r'^unavailable$', views.unavailable, name='unavailable'),
]