# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from intents.intent_engine import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def network_topology(request):
    return render(request, 'Network_Topology.html')


def testdb(request):
<<<<<<< HEAD
<<<<<<< HEAD
    c = ComputeAndPush('10.0.1.200', 'DEN', 'SFO', 'least_latency')
    db = c.intentEngine()
    return HttpResponse(db)
=======
=======
    c = ComputeAndPush('198.11.21.36', 'DEN', 'SFO', 'least_hop_count')
    db = c.intentEngine()
    return HttpResponse(db)

>>>>>>> 9de247b73bf824aaebd0a19764edc7156d521d1e
@api_view(['GET'])
def dropdown_data(request):
    """
    {'1':
        {
            'name' : 'Denver to Los Angeles - least latency',
            'path' : 'dpid - dpid -dpid',
        },
    '2':
        {
            'name' : 'Denver to Los Angeles - least latency',
            'path' : 'dpid - dpid -dpid',
        },
    }
    """
    data = {}
    try:
        if request.method == 'GET':
            intents_all = Intent_Data.objects.all()
            i=1
            for intent in intents_all:
                source = Customer.objects.filter(Prefix=intent.Source_IP).values_list('location',flat=True)[0]
                destination = Customer.objects.filter(Prefix=intent.Destination_IP).values_list('location',flat=True)[0]
                intent_type = intent.Intent_Type
                temp = {}
                temp['name'] = "{0} to {1} - {2}".format(source,destination,intent_type)
                temp['path'] = intent.Path
                data[i] = temp
                i += 1
            return HttpResponse(data)
    except:
<<<<<<< HEAD
        return Response(data)
>>>>>>> f7e8df6b245059931f3a06e9ce672d4489722cdc
=======
        return HttpResponse(data)
>>>>>>> 9de247b73bf824aaebd0a19764edc7156d521d1e
