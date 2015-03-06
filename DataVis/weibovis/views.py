# -*- coding:utf-8 -*-
import random
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.db.models import Max, Min
from weibovis.models import StatsData


def index(request):
    return HttpResponse("hello django \n <a href='/weibovis/about'>about</a>")


def about(request):
    # return HttpResponse("this is about page \n <a href='/weibovis/'>index</a>")
    return render_to_response('weibovis/about.html')


def mapdata(request):
    return render_to_response('weibovis/index.html')


def getdata(request):
    # deal with the request from front, now it is map data
    querydict = request.GET
    kind = querydict['kind']

    if kind == 'map':
        # construct map data
        result = get_map_data()
    return JsonResponse(result, safe=False)


def get_map_data():
    series_data = []
    stats_list = StatsData.objects.all()
    for item in stats_list:
        series_data.append(item.get_dict())
    result = dict()
    datarange = dict()
    # through the aggregate function to get max and min value
    # the result like {'pntcnt__max': 378}
    datarange['max'] = stats_list.aggregate(Max('pntcnt'))['pntcnt__max']
    datarange_min = stats_list.aggregate(Min('pntcnt'))['pntcnt__min']
    datarange['min'] = 0 if datarange_min > 0 else datarange_min
    result['series'] = series_data
    result['datarange'] = datarange
    return result


def make_data(places):
    data = []
    plen = len(places)
    for i in range(plen):
        geocoord = places[i]['geoCoord']
        data.append({
            'name': places[i]['name'],
            'value': 10,
            'geoCoord': [
                geocoord[0] + random.random() * 5 * -1,
                geocoord[1] + random.random() * 3 * -1
            ]
        })
    return data