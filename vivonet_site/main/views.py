# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

# Create your views here.
def index_view(request):
    return render(request, 'index.html')

def network_topology(request):
    return render(request, 'Network_Topology.html')