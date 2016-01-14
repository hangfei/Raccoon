from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_enverest/$', views.about_enverest, name='about_enverest'),
    url(r'^service/$', views.service, name='service'),
    url(r'^client_see_this/$', views.client_see_this, name='client_see_this'),
    url(r'^expert_see_this/$', views.expert_see_this, name='expert_see_this'),
]