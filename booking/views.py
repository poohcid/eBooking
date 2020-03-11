from datetime import date, datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .models import Booking, Room


#หน้าแรก
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

#จองห้อง
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


#ค้นหาห้องที่เวลาไม่ชนในวันนั้น
def booked_filter(date, start_time, end_time):
    books = Booking.objects.filter(date=date)
    list_book = list(books.filter(end_time__lt=start_time).filter(end_time__lt=end_time))
    list_book += list(books.filter(start_time__gt=start_time).filter(start_time__gt=end_time))
    booked = Booking.objects.exclude(pk__in=map(lambda x: x.id, list_book))
    booked = booked.filter(date=date)
    booked = booked.filter(status='อนุมัติ')
    return Room.objects.exclude(pk__in=map(lambda x: x.room.id, booked))


#บันทึกการจองแล้ว redirect ไปหน้าประวัติการจอง
@login_required
@permission_required('booking.add_booking')
def save_booking(request, id):
    context = {
        "room" : Room.objects.get(pk=id),
        "user" : request.user
    }
    if request.method == "POST":
        try:
            context["descrip"] = request.POST.get('descrip')
            room = Room.objects.get(pk=id)
            date = str(datetime.strptime(request.POST.get('date'), '%m/%d/%Y')).split()[0]
            start_time = datetime.time(datetime.strptime(request.POST.get('start_time'), '%H:%M'))
            end_time = datetime.time(datetime.strptime(request.POST.get('end_time'), '%H:%M'))
            
            if (room.open_time <= start_time and room.close_time >=  end_time) and (end_time > start_time) and \
                (room in booked_filter(date, start_time, end_time)): #ตรวจสอบห้องที่ยังไม่ได้จอง ในวันและเวลาที่เลือก

                book = Booking(
                    room = room,
                    date = date,
                    start_time = request.POST.get("start_time"),
                    end_time = request.POST.get("end_time"),
                    description = request.POST.get("descrip"),
                    book_by = request.user
                )
                book.save()
                return redirect('book_list')
            else:
                context["error"] = "ไม่สามารถจองในช่วงเวลาดังกล่าวได้ อาจจะเพราะเกินเวลาห้องหรือห้องนี้มีคนจองไปแล้ว"
                return render(request, 'booking.html', context=context)
        except ValueError:
            context["error"] = "โปรดกรอกวันและเวลาให้ถูกต้อง"
            return render(request, 'booking.html', context=context)
    else:
        return redirect('index')

#ดูประวัติการจอง
@login_required
@permission_required('booking.view_booking')
def book_list(request):
    context = {
        "books" : Booking.objects.filter(book_by=request.user).order_by('book_date')[::-1],
        "user" : request.user
    }
    return render(request, 'book_list.html', context=context)

#ค้นหาห้องที่เวลาไม่ทับกับเวลาที่ค้นหา
@login_required
def date_search(request):
    context = {
        "room" : Room.objects.all(),
        "user" : request.user
    }
    if request.method == 'GET':
        if (request.GET.get('date') and request.GET.get('start_time') and request.GET.get('end_time')):
            try:
                start_time = datetime.time(datetime.strptime(request.GET.get('start_time'), '%H:%M'))
                end_time = datetime.time(datetime.strptime(request.GET.get('end_time'), '%H:%M'))
                my_date = str(datetime.strptime(request.GET.get('date'), '%m/%d/%Y')).split()[0]

                context['room'] = booked_filter(
                    date = my_date,
                    start_time = start_time,
                    end_time = end_time
                )
                context['room'] = context['room'].filter(open_time__lte=start_time)
                context['room'] = context['room'].filter(close_time__gte=end_time)
                if request.GET.get('name'):
                    context['room'] = context['room'].filter(name__contains=request.GET.get('name'))
                if not my_date:
                    context['date'] = date.today
                else:
                    context['date'] = datetime.strptime(request.GET.get('date'), '%m/%d/%Y')
            except ValueError:
                context['error'] = 'โปรดกรอกวันและเวลาให้ถูกต้อง'
                return render(request, 'index.html', context=context)
        elif request.GET.get('name'):
            context['room'] = context['room'].filter(name__contains=request.GET.get('name'))
        else:
            context['error'] = 'โปรดกรอกวันและเวลาให้ครบถ้วน'
        return render(request, 'index.html', context=context)

#[admin] แก้ไขการจอง
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

def isRange_time(start_time, end_time):
    st = datetime.time(datetime.strptime(start_time, '%H:%M'))
    et = datetime.time(datetime.strptime(end_time, '%H:%M'))
    if st > et:
        print(111)
        return False
    return True

#[admin] ดูรายการห้อง
@login_required
@permission_required('booking.add_room')
def room_list(request):
    if request.method == "POST":
        try:
            room = Room(
                name = request.POST.get('name'),
                open_time = request.POST.get('open_time'),
                close_time = request.POST.get('close_time'),
                capacity = request.POST.get('capacity')
            )
            room.save()
        except ValidationError:
            context = {
                "user" : request.user,
                "room" : Room.objects.all(),
                'error' : 'โปรดใส่เวลาให้ถูกต้อง'
            }
            return render(request, 'admin_page/room_list.html', context=context)
    context = {
        "user" : request.user,
        "room" : Room.objects.all()
    }
    return render(request, 'admin_page/room_list.html', context=context)

#[admin] แก้ไขห้องและลบห้อง
@login_required
@permission_required('booking.change_room', 'booking.delete_booking')
def room_edit(request, id):
    try:
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
    except ValidationError:
        context['error'] = 'โปรดใส่เวลาให้ถูกต้อง'
        return render(request, 'admin_page/room_edit.html', context=context)

    except Room.DoesNotExist:
        return redirect('room_list')
