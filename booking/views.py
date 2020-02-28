from django.http import HttpResponse
from django.shortcuts import render


def book_index(request):
    return render(request, 'index.html', context={})

def page1(request, num):
    return HttpResponse('page %s' %num)