from django.conf.urls import patterns, url
from weibovis import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^mapdata/$', views.mapdata, name='mapdata'),
                       url(r'^getdata/$', views.getdata, name='getdata'),
                       url(r'^timedata/$', views.timedata, name='timedata'),
                       url(r'^charts/$', views.bardata, name='bardata'),
                       url(r'^line/$', views.linedata, name='linedata'))
