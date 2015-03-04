from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import loader, Context


def index(request):
    return HttpResponse("hello django \n <a href='/weibovis/about'>about</a>")


def about(request):
    # return HttpResponse("this is about page \n <a href='/weibovis/'>index</a>")
    return render_to_response('weibovis/about.html')


def mapdata(request):
    return render_to_response('weibovis/index.html')