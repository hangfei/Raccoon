from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='payment_index'),
    url(r'^bank_transfer/$', views.bank_transfer, name='bank_transfer'),
    url(r'^bank_transfer_detail/$', views.bank_transfer_detail, name='bank_transfer_detail'),
    url(r'^bank_transfer/bank_transfer_beijing/$', views.bank_transfer_beijing, name='bank_transfer_beijing'),
    url(r'^alipay/$', views.alipay, name='alipay'),
]