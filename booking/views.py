from datetime import date, datetime

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Booking, Room


def book_index(request):
    context = {
        "room" : Room.objects.all(),
        "date" : date.today
    }
    return render(request, 'index.html', context=context)

def booking(request, id, bdate):
    try:
        context={
            "room" : Room.objects.get(pk=id),
            "date" : date.fromisoformat(bdate)
        }
        return render(request, 'booking.html', context=context)
    except Room.DoesNotExist:
        return redirect('index')

def save_booking(request, id):
    if request.method == "POST":
        book = Booking(
            room = Room.objects.get(pk=id),
            date = str(datetime.strptime(request.POST.get('date'), '%m/%d/%Y')).split()[0],
            start_time = request.POST.get("start_time"),
            end_time = request.POST.get("end_time"),
            description = request.POST.get("descrip")
        )
        book.save()
        return redirect('book_list')
    else:
        return redirect('index')

def book_list(request):
    context = {
        "books" : Booking.objects.all()
    }
    return render(request, 'book_list.html', context=context)

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
