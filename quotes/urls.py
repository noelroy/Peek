from django.conf.urls import url
from . import views

app_name = 'quotes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^quote_list/$', views.quote_list, name='quote_list'),
    url(r'^quote_list/(?P<pk>\d+)/$', views.quote_detail, name='quote_detail'),
]
