from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urls_basics = [
    url(r'^$', index_view, name='index'),

]

urlpatterns = urls_basics