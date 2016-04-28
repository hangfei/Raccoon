from django.conf.urls import url

from . import views

app_name = 'homepage'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^service/$', views.service, name='service'),
    url(r'^how_it_works/$', views.how_it_works, name='how_it_works'),
    url(r'^news_blog/$', views.news_blog, name='news_blog'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^terms_of_service/$', views.terms_of_service, name='terms_of_service'),
    url(r'^join_us/$', views.join_us, name='join_us'),
    url(r'^client_see_this/$', views.client_see_this, name='client_see_this'),
    url(r'^expert_see_this/$', views.expert_see_this, name='expert_see_this'),
]