from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_enverest/$', views.about_enverest, name='about_enverest'),
    url(r'^service/$', views.service, name='service'),
    url(r'^how_it_works/$', views.how_it_works, name='how_it_works'),
    url(r'^member_benefits/$', views.member_benefits, name='member_benefits'),
    url(r'^team/$', views.team, name='team'),
    url(r'^partners/$', views.partners, name='partners'),
    url(r'^news_blog/$', views.news_blog, name='news_blog'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^success_story/$', views.success_story, name='success_story'),
    url(r'^client_see_this/$', views.client_see_this, name='client_see_this'),
    url(r'^expert_see_this/$', views.expert_see_this, name='expert_see_this'),
]