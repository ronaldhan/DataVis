from django.conf.urls import patterns, url
from weibovis import views


urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^about/$', views.about, name='about'),
                       url(r'^mapdata/$', views.mapdata, name='mapdata'),
                       url(r'^getdata/$', views.getdata, name='getdata'))
