from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    open_time = models.TimeField()
    close_time = models.TimeField()
    capacity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.PROTECT, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True)
    description = models.TextField()
    status = models.CharField(null=True, default=None, choices=(
        ("รออนุมัติ", "Unknow"),
        ("ไม่อนุมัติ", "No"),
        ("อนุมัติ", "Yes")
    ), max_length=100)
    status_remark = models.TextField(null=True, blank=True)
    book_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.room.name
