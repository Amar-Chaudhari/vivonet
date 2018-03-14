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
    c = ComputeAndPush('10.0.1.200', 'DEN', 'SFO', 'least latency')
    db = c.intentEngine()
    return HttpResponse(db)
