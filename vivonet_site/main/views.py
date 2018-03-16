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
from django.views.decorators.csrf import csrf_exempt, csrf_protect


# Create your views here.
def index_view(request):
    return render(request, 'index.html')


def network_topology(request):
    return render(request, 'Network_Topology.html')


def testdb(request):
    c = ComputeAndPush('10.0.1.200', 'DEN', 'SFO', 'least_latency')
    db = c.intentEngine()
    return HttpResponse(db)

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
    data = []
    try:
        if request.method == 'GET':
            intents_all = Intent_Data.objects.all()
            for intent in intents_all:
                source = Customer.objects.filter(Prefix=intent.Source_IP).values_list('location', flat=True)[0]
                destination = Customer.objects.filter(Prefix=intent.Destination_IP).values_list('location', flat=True)[
                    0]
                intent_type = intent.Intent_Type
                temp = {}
                temp['name'] = "{0} to {1} - {2}".format(source, destination, intent_type)
                temp['path'] = intent.Path
                data.append(temp)
            return Response(data)
    except:
        return Response(data)
        
@api_view(['GET'])
def customer_data(request):     

    """
    { 
      '20.0.0.1' : 'DEN',
      '20.0.0.2' : 'SFO'
    }
    """
    data = []
    try:
        if request.method == 'GET':
            intents_all = Intent_Data.objects.all()
            for intent in intents_all:
                location = Customer.objects.filter(Prefix=intent.Source_IP).values_list('location', flat=True)[0]
                temp = {}
                temp[intent.Source_IP] = location
                data.append(temp)
            return Response(data)
    except:
        return Response(data)
    