from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urls_basics = [
    url(r'^$', index_view, name='index'),
    url('topology',network_topology, name='index'),
    url('testdb',testdb),

]

urlpatterns = urls_basics