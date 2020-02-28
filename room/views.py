from django.http import HttpResponse
from django.shortcuts import render


def page2(request):
    return HttpResponse("page2")
