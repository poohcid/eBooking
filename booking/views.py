from datetime import date

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Room


def book_index(request):
    context = {
        "room" : Room.objects.all(),
        "date" : date.today
    }
    return render(request, 'index.html', context=context)

def booking(request, id):
    try:
        context={
            "room" : Room.objects.get(pk=id)
        }
        return render(request, 'booking.html', context=context)
    except Room.DoesNotExist:
        return redirect('index')

def date_search(request):
    context = {
        "room" : Room.objects.all()
    }
    if request.method == 'GET':
        my_date = request.GET.get('date')
        if not my_date:
            context['date'] = date.today
        else:
            context['date'] = date.fromisoformat(my_date)
        return render(request, 'index.html', context=context)
