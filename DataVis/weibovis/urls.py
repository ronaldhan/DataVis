from django.conf.urls import patterns, url
from weibovis import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^mapdata/$', views.mapdata, name='mapdata'),
                       url(r'^getdata/$', views.getdata, name='getdata'),
                       url(r'^getheatmapdata/$', views.getheatmapdata, name='getheatmapdata'),
                       url(r'^getpathdata/$', views.getpathdata, name='getpathdata'),
                       url(r'^time/$', views.timedata, name='timedata'),
                       url(r'^charts/$', views.bardata, name='bardata'),
                       url(r'^line/$', views.linedata, name='linedata'),
                       url(r'^workday/$', views.workdaydata, name='workdaydata'),
                       url(r'^worknight/$', views.worknightdata, name='worknightdata'),
                       url(r'^timegif/$', views.timegif, name='timegif'),
                       url(r'^hm/map/$', views.hmmap, name='hmmap'),
                       url(r'^hotmap/$', views.hotmap, name='hotmap'),
                       url(r'^kde/$', views.kde, name='kde'),
                       url(r'^path/$', views.path, name='path'),
                       url(r'^register/$', views.register, name='register'))
