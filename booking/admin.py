from django.contrib import admin
from django.contrib.auth.models import Permission
from . import models

admin.site.register(Permission)

admin.site.register(models.Room)

admin.site.register(models.Booking)
