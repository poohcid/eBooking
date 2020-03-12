from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_index, name="index"), #index
    path('search/', views.date_search, name="date_search"), #ค้าหาห้อง
    path('booking/<int:id>/', views.booking, name="booking"), #หน้าจองห้อง input เป็น id ห้อง
    path('save_booking/<int:id>/', views.save_booking, name="save_booking"), #บันทึกการจอง input เป็น id ห้อง
    path('book_list/', views.book_list, name="book_list"), #หน้าข้อมูลการจอง

    path('book_edit/<int:id>/', views.book_edit, name="book_edit"), #admin แก้ไขการจอง
    path('room_list/', views.room_list, name="room_list"), #admin แสดงห้อง เพิ่มห้อง
    path('room_edit/<int:id>/', views.room_edit, name="room_edit") #admin แก้ไขห้อง ลบห้อง
]