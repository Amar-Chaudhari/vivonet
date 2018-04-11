# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
from intents.intent_engine import *

logger = logging.getLogger(__name__)

# Create your views here.
@login_required
def index_view(request):
    LOGGED_IN_USER = request.user.username
    return render(request, 'index.html')


@login_required
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
                    if intents_all[i].From_Location == intents_all[i + 1].To_Location and intents_all[i].To_Location == \
                            intents_all[i + 1].From_Location:
                        source = \
                            Customer.objects.filter(Prefix=intents_all[i].Source_IP).values_list('location', flat=True)[
                                0]
                        destination = \
                            Customer.objects.filter(Prefix=intents_all[i].Destination_IP).values_list('location',
                                                                                                      flat=True)[
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


@login_required
def intentengine(request):
    if request.method == "GET":
        return render(request, 'intent_engine.html')
    elif request.method == "POST":
        error = False
        try:
            intent_type = request.POST.get('intent_type')
            from_city = request.POST.get('source_location')
            to_city = request.POST.get('destination_location')
            if intent_type and from_city and to_city:

                supported_locations = Customer.objects.values_list('location', flat=True)
                supported_locations_lower = map(lambda x: x.lower(), supported_locations)

                if from_city.lower() == to_city.lower():
                    error = True
                elif from_city.lower() not in supported_locations_lower or to_city.lower() not in supported_locations_lower:
                    error = True
                else:
                    c = ComputeAndPush('10.0.1.200', from_city, to_city, intent_type)
                    status = c.intentEngine()

                    c2 = ComputeAndPush('10.0.1.200', to_city, from_city, intent_type)
                    status2 = c2.intentEngine()

                    if status is not False and status2 is not False:
                        error = False
                        succeed = True
                    else:
                        error = True
                return render(request, 'intent_engine.html', {'error': error,'succeed': succeed})
        except Exception as e:
            error = True
            logging.error(e)
    return render(request, 'intent_engine.html', {'error': error})
