from django.conf.urls import url
from django.contrib.auth import views as auth_views
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings

from main.views import *

urls_basics = [
    url(r'^$', index_view, name='index'),
    url('^topology', network_topology, name='topology'),
    url('^testdb', testdb),
    url('api/dropdown_data$', dropdown_data),
    url('api/customer_data$', customer_data),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url('^intentengine/$', intentengine,name='intent_engine'),
]

urlpatterns = urls_basics

urlpatterns = format_suffix_patterns(urlpatterns)
