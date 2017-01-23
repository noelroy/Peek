from django.conf.urls import url
from . import views

app_name = 'quotes'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),

    url(r'^edit_profile/$', views.update_profile, name='update_profile'),
    url(r'^profile/(?P<pk>\d+)/$', views.profile, name='profile_detail'),

    url(r'^create_quote/$', views.create_quote, name='create_quote'),
    url(r'^quote_list/(?P<pk>\d+)/$', views.QuoteUpdate.as_view(), name='update_quote'),
    url(r'^quote_list/$', views.quote_list, name='quote_list'),
    #url(r'^quote_list/(?P<pk>\d+)/$', views.quote_detail, name='quote_detail'),
    url(r'^quote_list/(?P<pk>\d+)/delete_quote/$', views.delete_quote, name='delete_quote'),
]
