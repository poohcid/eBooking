from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_index, name="index"),
    path('search/', views.date_search, name="date_search"),
    path('booking/<int:id>/', views.booking, name="booking")
]