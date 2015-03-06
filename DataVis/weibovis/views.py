# -*- coding:utf-8 -*-
import random
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
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
        print JsonResponse(result, safe=False)
    return JsonResponse(result, safe=False)


def get_map_data():
    # series_data = [
    #     {'name': 1, 'value': 10, 'geoCoord': [116.090316745, 39.8066538017]},
    #     {'name': 2, 'value': 10, 'geoCoord': [116.14783293, 39.8037860467]},
    #     {'name': 3, 'value': 10, 'geoCoord': [116.168974437, 39.8040199854]},
    #     {'name': 4, 'value': 10, 'geoCoord': [116.154235095, 39.8162342218]},
    #     {'name': 5, 'value': 10, 'geoCoord': [116.180089174, 39.8079383742]},
    #     {'name': 6, 'value': 10, 'geoCoord': [116.148811202, 39.8080363974]}
    # ]
    series_data = []
    stats_list = StatsData.objects.all()
    for item in stats_list:
        series_data.append(item.get_dict)
    result = dict()
    result['series'] = series_data
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