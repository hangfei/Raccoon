from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_enverest/$', views.about_enverest, name='about_enverest'),
    url(r'^service/$', views.service, name='service'),
]