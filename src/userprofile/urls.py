from django.conf.urls import url
from . import views
# from userprofile.views import UserprofileUpdate

urlpatterns = [
	url(r"^edit/$", views.userprofile_edit, name="userprofile_update"),
	# url(r'^(?P<username>\w+)/edit/$', UserprofileUpdate.as_view(), name='userprofile_update'),
	url(r'^(?P<username>\w+)/$', views.user_profile, name='user_profile'),
]
