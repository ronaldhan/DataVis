from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader, Context


def index(request):
    return HttpResponse("hello django \n <a href='/weibovis/about'>about</a>")


def about(request):
    # return HttpResponse("this is about page \n <a href='/weibovis/'>index</a>")
    return render_to_response('weibovis/about.html')


def mapdata(request):
    t = loader.get_template('static/doc/example/mapdata.html')
    c = Context({
        'mapdata': mapdata,
    })
    return HttpResponse(t.render(c))