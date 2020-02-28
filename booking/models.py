from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    open_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

