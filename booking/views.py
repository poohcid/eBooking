from datetime import date, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Booking, Room


@login_required
def book_index(request):
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
def booking(request, id):
    try:
        context={
            "room" : Room.objects.get(pk=id),
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
        start_time = datetime.time(datetime.strptime(request.GET.get('start_time'), '%H:%M'))
        end_time = datetime.time(datetime.strptime(request.GET.get('end_time'), '%H:%M'))
        my_date = request.GET.get('date')
        books = Booking.objects.filter(date=str(datetime.strptime(my_date, '%m/%d/%Y')).split()[0])
        list_book = list(books.filter(end_time__lt=start_time).filter(end_time__lt=end_time))
        list_book += list(books.filter(start_time__gt=start_time).filter(start_time__gt=end_time))
        print(list_book)
        if not my_date:
            context['date'] = date.today
        else:
            context['date'] = datetime.strptime(my_date, '%m/%d/%Y')
        return render(request, 'index.html', context=context)

def book_login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        passwprd = request.POST.get('password')
        user = authenticate(request, username=username, password=passwprd)
        if user:
            login(request, user)
            return redirect('index')
        else:
            context['error'] = 'รหัสผ่านไม่ถูกต้อง'
    return render(request, 'login.html', context=context)

def book_sign_in(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            try:
                user = User.objects.create_user(
                    username = request.POST.get('username'),
                    email = request.POST.get('email'),
                    password = request.POST.get('password1')
                )
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                my_group = Group.objects.get(name='member')
                user.groups.add(my_group)
                user.save()
                login(request, user)
                return redirect('index')
            except IntegrityError:
                context['error'] = 'ชื่อนี้มีคนใช้ไปแล้ว'
        else:
            context['error'] = 'โปรดกรอกรหัสให้ตรงกัน'
    return render(request, 'sign_in.html', context=context)

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
        return redirect('index')
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
    context = {
        "room" : Room.objects.get(pk=id)
    }
    if request.method == "POST":
        room = context["room"]
        if request.POST.get('delete'):
            room.delete()
            return redirect('room_list')
        else:
            room.name = request.POST.get('name')
            room.open_time = request.POST.get('open_time')
            room.close_time = request.POST.get('close_time')
            room.capacity = request.POST.get('capacity')
            room.save()
            return redirect('room_list')
    return render(request, 'admin_page/room_edit.html', context=context)
