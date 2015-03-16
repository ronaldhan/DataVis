# -*- coding:utf-8 -*-
import os
import numpy as np

from django.conf import settings
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.db.models import Max, Min

import pysal.esda.mapclassify as mpc

from weibovis.models import StatsData, Grid, WbPoint
from weibovis.utils import store_json, read_json


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
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'map_data.json'
    full_path = os.path.join(file_folder, file_name)

    # check if the result json file exists
    # if it exists, read the file and return, else compute the result and store
    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        series_data = dict()
        result = dict()
        datarange = dict()
        high = []
        middle = []
        low = []
        values = []

        stats_list = StatsData.objects.all()

        for item in stats_list:
            values.append(item.get_value())
        # need to transform the python list to numpy array to use the copy attribution
        values = np.asarray(values)
        nbreaks = get_data_breaks(values, k=3)
        print nbreaks
        for item in stats_list:
            pntcnt = item.get_value()
            if pntcnt < nbreaks[0]:
                low.append(item.get_dict())
            elif pntcnt > nbreaks[1]:
                high.append(item.get_dict())
            else:
                middle.append(item.get_dict())

        # through the aggregate function to get max and min value
        # the result like {'pntcnt__max': 378}
        datarange['max'] = stats_list.aggregate(Max('pntcnt'))['pntcnt__max']
        datarange_min = stats_list.aggregate(Min('pntcnt'))['pntcnt__min']
        datarange['min'] = 0 if datarange_min > 0 else datarange_min

        series_data['high'] = high
        series_data['middle'] = middle
        series_data['low'] = low

        result['series'] = series_data
        result['datarange'] = datarange

        store_json(result)
    return result


def get_data_breaks(y, k=5):
    """
    get the stats array and compute the natural jenks breaks of this array
    :param y: the array or iterable object
    :param k: the class number to be breaked
    :return: array (k,1), the upper bounds of each class
    """
    nb = mpc.Natural_Breaks(y, k=k)
    return nb.bins


def get_time_data():
    """
    compute the time range data
    :return:dict object contains
    """
    date_column = 'cdate'
    grids = Grid.objects.all()
    dates = WbPoint.objects.order_by(date_column).distinct(date_column)
    # final result
    result = dict()
    # day_item one grid in one day's count
    day_item = dict()
    # store all days data
    all_day = dict()
    # date string list
    date_list = [cdate.cdate.strftime('%Y-%m-%d') for cdate in dates]

    for cdate in dates:
        one_date = cdate.cdate
        date_str = cdate.cdate.strftime('%Y-%m-%d')
        # day_data all grids in one day's count
        day_data = []
        for grid in grids:
            # compute the point within the grid
            # get the weibo point in one day and in the special grid
            points = WbPoint.objects.filter(point__within=grid.geom).filter(cdate=one_date)
            pntcnt = len(points)
            day_item['name'] = grid.rid
            day_item['value'] = pntcnt
            day_item['geoCoord'] = [grid.x, grid.y]
            day_data.append(day_item)
        all_day[date_str] = day_data
    result['series'] = all_day
    result['timeline'] = date_list

    return result
