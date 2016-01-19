"""enverest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('homepage.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r"^account/", include("account.urls")),
    url(r"^consultant/", include("consultant.urls")),
    url(r"^search/", include("search.urls")),
    url(r"^project/", include("project.urls")),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include("userprofile.urls")),
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
    url(r'^payment/', include('payment.urls', namespace='payment', app_name='payment')),
]
