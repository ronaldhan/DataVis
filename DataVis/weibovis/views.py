from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("hello django \n <a href='/weibovis/about'>about</a>")


def about(request):
    return HttpResponse("this is about page \n <a href='/weibovis/'>index</a>")
