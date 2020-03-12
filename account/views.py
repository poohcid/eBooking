from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.db import IntegrityError
from django.shortcuts import redirect, render

def book_login(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        passwprd = request.POST.get('password')
        user = authenticate(request, username=username, password=passwprd)
        if user:
            login(request, user)
            return redirect('/')
        else:
            context['error'] = 'รหัสผ่านไม่ถูกต้อง'
    return render(request, 'login.html', context=context)

def book_register(request):
    context = {}
    if request.user.is_authenticated:
        return redirect('/')
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
                return redirect('/')
            except IntegrityError:
                context['error'] = 'ชื่อนี้มีคนใช้ไปแล้ว'
        else:
            context['error'] = 'โปรดกรอกรหัสให้ตรงกัน'
    return render(request, 'register.html', context=context)

@login_required
def book_logout(request):
    logout(request)
    return redirect('login')
