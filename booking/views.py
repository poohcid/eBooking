from datetime import date, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Booking, Room


@login_required
def book_index(request):
    print(request.user.groups.all())
    if request.user.is_superuser:
        return redirect("admin/")
    context = {"user" : request.user}
    if str(request.user.groups.all()[0]) == "member":
        context["room"] = Room.objects.all()
        context["date"] = date.today
        return render(request, 'index.html', context=context)

    #หน้าผู้ดูแล
    else:
        context["books"] = Booking.objects.all().order_by('book_date')[::-1]
        return render(request, 'admin_page/book_request.html', context=context)
@login_required
@permission_required('booking.add_booking')
def booking(request, id, bdate):
    try:
        context={
            "room" : Room.objects.get(pk=id),
            "date" : date.fromisoformat(bdate),
            "user" : request.user
        }
        return render(request, 'booking.html', context=context)
    except Room.DoesNotExist:
        return redirect('index')

@login_required
@permission_required('booking.add_booking')
def save_booking(request, id):
    if request.method == "POST":
        book = Booking(
            room = Room.objects.get(pk=id),
            date = str(datetime.strptime(request.POST.get('date'), '%m/%d/%Y')).split()[0],
            start_time = request.POST.get("start_time"),
            end_time = request.POST.get("end_time"),
            description = request.POST.get("descrip"),
            book_by = request.user
        )
        book.save()
        return redirect('book_list')
    else:
        return redirect('index')

@login_required
@permission_required('booking.view_booking')
def book_list(request):
    context = {
        "books" : Booking.objects.filter(book_by=request.user).order_by('book_date')[::-1],
        "user" : request.user
    }
    return render(request, 'book_list.html', context=context)

@login_required
def date_search(request):
    context = {
        "room" : Room.objects.all(),
        "user" : request.user
    }
    if request.method == 'GET':
        my_date = request.GET.get('date')
        if not my_date:
            context['date'] = date.today
        else:
            context['date'] = date.fromisoformat(my_date)
        return render(request, 'index.html', context=context)

def book_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwprd = request.POST.get('password')
        user = authenticate(request, username=username, password=passwprd)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html', context={})

@login_required
def book_logout(request):
    logout(request)
    return redirect('login')

@login_required
@permission_required('booking.change_booking')
def book_edit(request, id):
    book = Booking.objects.get(pk=id)
    if request.method == 'POST':
        book.status = request.POST.get('status')
        book.status_remark = request.POST.get('status-remark')
        book.save()
    context={
        "book" : book
    }
    return render(request, 'admin_page/book_edit.html', context=context)

@login_required
def room_list(request):
    if request.method == "POST":
        room = Room(
            name = request.POST.get('name'),
            open_time = request.POST.get('open_time'),
            close_time = request.POST.get('close_time'),
            capacity = request.POST.get('capacity')
        )
        room.save()
    context = {
        "user" : request.user,
        "room" : Room.objects.all()
    }
    return render(request, 'admin_page/room_list.html', context=context)

def room_edit(request, id):
    pass