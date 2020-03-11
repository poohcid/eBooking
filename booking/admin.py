from django.contrib import admin
from django.contrib.auth.models import Permission
from . import models

class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'status']

admin.site.register(Permission)

admin.site.register(models.Room)

admin.site.register(models.Booking, BookingAdmin)
