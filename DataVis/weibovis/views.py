# -*- coding:utf-8 -*-
from __future__ import division
import os
import numpy as np
import copy
from itertools import chain, islice

from django.conf import settings
from django.db import connection
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.db.models import Max, Min

import pysal.esda.mapclassify as mpc

from weibovis.models import StatsData, Grid, WbPoint, UserCount, WbPointPop
from weibovis.utils import store_json, read_json


def index(request):
    return HttpResponse('weibovis/about.html')


def about(request):
    return render_to_response('weibovis/about.html')


def mapdata(request):
    return render_to_response('weibovis/index.html')


def timedata(request):
    return render_to_response('weibovis/time.html')


def timegif(request):
    return render_to_response('weibovis/time-pic.html')


def bardata(request):
    return render_to_response('weibovis/charts.html')


def linedata(request):
    return render_to_response('weibovis/line.html')


def workdaydata(request):
    return render_to_response('weibovis/workday.html')


def worknightdata(request):
    return render_to_response('weibovis/worknight.html')


def hmmap(request):
    return render_to_response('weibovis/hm-map.html')


def hotmap(request):
    return render_to_response('weibovis/hotmap.html')


def kde(request):
    return render_to_response('weibovis/kde.html')


def getdata(request):
    # deal with the request from front, now it is map data
    querydict = request.GET
    kind = querydict['kind']

    if kind == 'map':
        # construct map data
        result = get_map_data()
    elif kind == 'time':
        result = get_time_data()
    elif kind == 'bar':
        result = get_bar_data()
    elif kind == 'line':
        result = get_line_data()
    elif kind == 'workday':
        result = get_workday_data()
    elif kind == 'worknight':
        result = get_worknight_data()
    else:
        pass
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

        store_json(file_name, result, folder_path=file_folder)
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
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'time_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        date_column = 'cdate'
        grids = Grid.objects.all()
        dates = WbPoint.objects.order_by(date_column).distinct(date_column)
        # final result
        result = dict()
        # store all days data
        all_day = dict()
        # date string list
        date_list = [cdate.cdate.strftime('%Y-%m-%d') for cdate in dates]
        # data range
        datarange = dict()
        range_max = 0

        for cdate in dates:
            one_date = cdate.cdate
            date_str = one_date.strftime('%Y-%m-%d')
            # day_data all grids in one day's count
            day_data = []
            for grid in grids:
                # compute the point within the grid
                # get the weibo point in one day and in the special grid
                points = WbPoint.objects.filter(cdate=one_date)
                # print len(points)
                inp = points.filter(point__within=grid.geom)
                # print len(inp)
                # print grid.geom, grid.x, grid.y
                day_item = dict()
                pntcnt = inp.count()
                range_max = max(pntcnt, range_max)
                day_item['name'] = grid.rid
                day_item['value'] = pntcnt
                day_item['geoCoord'] = [grid.x, grid.y]
                # print day_item
                day_data.append(day_item)
            all_day[date_str] = day_data

        datarange['max'] = range_max
        datarange['min'] = 0

        result['series'] = all_day
        result['timeline'] = date_list
        result['datarange'] = datarange

        store_json(file_name, result, folder_path=file_folder)

    return result


def get_bar_data():
    """
    compute the data of night and day
    :return: dict contains all to display
    """
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'bar_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        date_column = 'cdate'
        dates = WbPoint.objects.order_by(date_column).distinct(date_column)
        # date string list
        date_list = [cdate.cdate.strftime('%Y-%m-%d') for cdate in dates]
        # final result
        result = dict()
        series = dict()
        day_list = []
        night_list = []
        total_list = []

        for cdate in dates:
            one_date = cdate.cdate
            points = WbPoint.objects.filter(cdate=one_date)
            total_item = points.count()
            inp = points.extra(where=['extract(hour from ctime) > 8']).extra(where=['extract(hour from ctime) < 22'])
            day_item = inp.count()
            night_item = total_item - day_item
            day_list.append(day_item)
            night_list.append(night_item)
            total_list.append(total_item)

        series['day'] = day_list
        series['night'] = night_list
        series['total'] = total_list
        series['xaxis'] = date_list

        result['series'] = series

        store_json(file_name, result, folder_path=file_folder)

    return result


def get_line_data():
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'line_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        series = dict()
        result = dict()
        xaxis = [i for i in range(1, 25, 2)]
        work_tmp_list = [0 for i in range(12)]
        end_tmp_list = [0 for i in range(12)]

        for day in range(1, 8):
            points = WbPoint.objects.filter(cdate__week_day=day)
            # compute how many days are this weekday
            dates = points.distinct('cdate')
            weekday_count = dates.count()
            day_list = []
            for middle in range(1, 25, 2):
                inp = points.extra(where=['extract(hour from ctime) in (%s, %s)' % (str(middle - 1), str(middle))])
                hour_item = inp.count()
                day_list.append(hour_item)

            for j in range(12):
                day_list[j] /= weekday_count

            series['t%s' % str(day)] = day_list

            day_list_copy = copy.copy(day_list)
            for i in range(12):
                if day < 6:
                    work_tmp_list[i] += day_list_copy[i]
                else:
                    end_tmp_list[i] += day_list_copy[i]

        work_tmp_list[i] /= 5
        end_tmp_list[i] /= 2

        series['workday'] = work_tmp_list
        series['weekend'] = end_tmp_list
        series['xaxis'] = xaxis

        result['series'] = series

        store_json(file_name, result, folder_path=file_folder)

    return result


def get_workday_data():
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'workday_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        series_data = dict()
        result = dict()
        high = []
        middle = []
        low = []
        datarange = dict()
        range_max = 0
        day_data = []
        stats_list = []

        # get the data in workday
        # week_day lookup return integer in [1,7], the sunday is 1 and saturday is 6
        points = WbPoint.objects.extra(select={'weekday': "cdate__week_day > 1"}).extra(select={'weekday': "cdate__week_day < 7"})
        # get the data in work time, 9-17
        inp = points.extra(where=['extract(hour from ctime) > 8']).extra(where=['extract(hour from ctime) < 18'])
        # get all the girds
        grids = Grid.objects.all()

        for grid in grids:
            dnp = inp.filter(point__within=grid.geom)
            day_item = dict()
            pntcnt = dnp.count()
            range_max = max(pntcnt, range_max)
            day_item['name'] = grid.rid
            day_item['value'] = pntcnt
            day_item['geoCoord'] = [grid.x, grid.y]
            day_data.append(day_item)
            stats_list.append(pntcnt)

        # need to transform the python list to numpy array to use the copy attribution
        values = np.asarray(stats_list)
        nbreaks = get_data_breaks(values, k=3)

        for i in range(len(stats_list)):
            pn = stats_list[i]
            if pn < nbreaks[0]:
                low.append(day_data[i])
            elif pn > nbreaks[1]:
                high.append(day_data[i])
            else:
                middle.append(day_data[i])

        datarange['max'] = range_max
        datarange['min'] = 0

        series_data['high'] = high
        series_data['middle'] = middle
        series_data['low'] = low

        result['series'] = series_data
        result['datarange'] = datarange

        store_json(file_name, result, folder_path=file_folder)
    return result


def get_worknight_data():
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'worknight_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        series_data = dict()
        result = dict()
        high = []
        middle = []
        low = []
        datarange = dict()
        range_max = 0
        day_data = []
        stats_list = []

        # get the data in workday
        # week_day lookup return integer in [1,7], the sunday is 1 and saturday is 6
        points = WbPoint.objects.extra(select={'weekday': "cdate__week_day > 1"}).extra(select={'weekday': "cdate__week_day < 7"})
        # get the data in work time, 9-17
        inp = points.extra(where=['extract(hour from ctime) < 8 OR extract(hour from ctime) > 18'])
        # inp2 = points.extra(select={'hour': "ctime__hour > 18"})

        # get all the girds
        grids = Grid.objects.all()

        for grid in grids:
            dnp = inp.filter(point__within=grid.geom)
            day_item = dict()
            pntcnt = dnp.count()
            range_max = max(pntcnt, range_max)
            day_item['name'] = grid.rid
            day_item['value'] = pntcnt
            day_item['geoCoord'] = [grid.x, grid.y]
            day_data.append(day_item)
            stats_list.append(pntcnt)

        # need to transform the python list to numpy array to use the copy attribution
        values = np.asarray(stats_list)
        nbreaks = get_data_breaks(values, k=3)

        for i in range(len(stats_list)):
            pn = stats_list[i]
            if pn < nbreaks[0]:
                low.append(day_data[i])
            elif pn > nbreaks[1]:
                high.append(day_data[i])
            else:
                middle.append(day_data[i])

        datarange['max'] = range_max
        datarange['min'] = 0

        series_data['high'] = high
        series_data['middle'] = middle
        series_data['low'] = low

        result['series'] = series_data
        result['datarange'] = datarange

        store_json(file_name, result, folder_path=file_folder)
    return result


def getheatmapdata(request):
    # deal with the request from front, now it is map data
    querydict = request.GET
    kind = querydict['kind']

    if kind == 'map':
        # construct map data
        result = get_hm_map_data()
    else:
        pass

    return JsonResponse(result, safe=False)


def get_hm_map_data():
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'hm_map_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        series_data = dict()
        result = dict()
        values = []

        stats_list = StatsData.objects.all()

        for item in stats_list:
            values.append(item.get_dict_xy())

        cmax = stats_list.aggregate(Max('pntcnt'))['pntcnt__max']

        series_data['max'] = cmax
        series_data['min'] = 0
        series_data['data'] = values

        result['series'] = series_data

        store_json(file_name, result, folder_path=file_folder)
    return result


def getpathdata(request):
    # deal with the request from front, now it is map data
    querydict = request.GET
    kind = querydict['kind']

    if kind == 'path':
        # construct map data
        result = get_path_data()
    else:
        pass

    return JsonResponse(result, safe=False)


def get_path_data():
    file_folder = os.path.join(settings.STATIC_PATH, 'Temple')
    file_name = 'path_data.json'
    full_path = os.path.join(file_folder, file_name)

    if os.path.exists(full_path):
        result = read_json(full_path)
    else:
        series_data = dict()
        result = dict()

        # get the top 50 users
        users = UserCount.objects.all()[:50]
        for user in users:
            # get all the records from pop table and order by datetime
            # this example shows how to use the postgis function in the queryset
            # using the values function to return json formatter result like
            # [{'y': 39.84944, 'x': 116.38768, 'uid': 3307285955L}, , ,]
            # user_records = WbPointPop.objects.filter(uid=user.uid).order_by('cdate', 'ctime').extra(
            #     select={
            #         'x': 'st_x("point")',
            #         'y': 'st_y("point")'
            #     }).values('uid', 'x', 'y')
            # use the connection to execute raw sql to get result
            cursor = connection.cursor()
            cursor.execute('select st_x(point) as x, st_y(point) as y '
                           'from weibovis_wbpointpop where uid = %s group by point '
                           'order by min(created_at)', [user.uid])
            # the points is a array, the uid is used as key
            points = cursor.fetchall()
            series_data['%s' % user.uid] = points

        result['series'] = series_data

        store_json(file_name, result, folder_path=file_folder)
    return result
