from django.conf.urls import url

#from . import views
from search.views import ExpertDetailView, ExpertListView

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    #url(r'^$', ExpertListView.as_view(), name='expert-list'),
    url(r'^$', ExpertListView.as_view(), name='expert-list'),
    url(r'^(?P<pk>[\w]+)/detail$', ExpertDetailView.as_view(), name='expert-detail'),
    #url(r'^search/(?P<lastname>.+)$', ExpertListView.as_view(), name='expert-list'),
]