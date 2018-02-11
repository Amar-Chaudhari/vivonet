from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from main.views import *


urls_basics = [
    url(r'^$', index_view, name='index'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urls_basics