from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_index, name="index"),
    path('search/', views.date_search, name="date_search"),
    path('booking/<int:id>/<bdate>', views.booking, name="booking"),
    path('save_booking/<int:id>/', views.save_booking, name="save_booking"),
    path('book_list/', views.book_list, name="book_list"),
    path('book_login/', views.book_login, name="login"),
    path('book_logout/', views.book_logout, name="logout"),
    path('book_edit/<int:id>/', views.book_edit, name="book_edit"),
    path('room_list/', views.room_list, name="room_list"),
    path('room_edit/<int:id>/', views.room_edit, name="room_edit")
]