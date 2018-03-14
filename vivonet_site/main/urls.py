from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from main.views import *

urls_basics = [
    url(r'^$', index_view, name='index'),
    url('topology', network_topology, name='index'),
    url('testdb', testdb),
    url('api/dropdown_data$', dropdown_data),

]

urlpatterns = urls_basics

urlpatterns = format_suffix_patterns(urlpatterns)