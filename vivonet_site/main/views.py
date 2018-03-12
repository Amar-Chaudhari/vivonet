# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

from main.models import *

from intents.intent_engine import *

# Create your views here.
def index_view(request):
    return render(request, 'index.html')

def network_topology(request):
    return render(request, 'Network_Topology.html')

def testdb(request):
    c = ComputeAndPush('198.11.21.36', 'DEN', 'SFO', 'least_hop_count')
    db = c.intentEngine()
    return HttpResponse(db)