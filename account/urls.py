from django.urls import path
from . import views

urlpatterns = [
    path('book_login/', views.book_login, name='login'),
    path('book_register/', views.book_register, name='register'),
    path('book_logout/', views.book_logout, name='logout')
]