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
    c = ComputeAndPush('10.0.1.200', 'DENVER', 'SAN FRANCISCO', 'high_bandwidth')
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
            skip = False
            i = 0
            while i < len(intents_all):
                if skip:
                    skip = False
                    pass
                else:
                    if intents_all[i].From_Location == intents_all[i+1].To_Location and intents_all[i].To_Location == intents_all[i+1].From_Location:
                        source = Customer.objects.filter(Prefix=intents_all[i].Source_IP).values_list('location', flat=True)[0]
                        destination = \
                        Customer.objects.filter(Prefix=intents_all[i].Destination_IP).values_list('location', flat=True)[
                            0]
                        intent_type = intents_all[i].Intent_Type
                        temp = {}
                        temp['name'] = "{0} to {1} - {2}".format(source, destination, intent_type)
                        temp['path'] = intents_all[i].Path
                        data.append(temp)
                        skip = True
                i += 1
            """
            for intent in intents_all:
                if skip:
                    skip = False
                    pass
                for temp in intents_all:
                        if intent.From_Location == temp.To_Location and intent.To_Location == temp.From_Location:
                            source = Customer.objects.filter(Prefix=intent.Source_IP).values_list('location', flat=True)[0]
                            destination = Customer.objects.filter(Prefix=intent.Destination_IP).values_list('location', flat=True)[
                                0]
                            intent_type = intent.Intent_Type
                            temp = {}
                            temp['name'] = "{0} to {1} - {2}".format(source, destination, intent_type)
                            temp['path'] = intent.Path
                            data.append(temp)
                            skip = True
                            break
            """
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
    data = {}
    try:
        if request.method == 'GET':
            cust_data = Customer.objects.all()
            for c in cust_data:
                data[c.Connected_Host] = c.location

        return Response(data)
        
    except:
        return Response(data)

@api_view(['GET'])
def login(request):		
    return render(request, 'login.html')
	
@api_view(['GET'])
def intentengine(request):		
    return render(intentengine, 'intent_engine.html')