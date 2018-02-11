# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

# Create your views here.
def index_view(request):
    #return render(request, 'index.html', {'title': title, 'meta_description': meta_description})
    return HttpResponse("Hello world")
