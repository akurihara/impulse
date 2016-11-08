from django.db import models


class Monitor(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime_event_start = models.DateTimeField(auto_now=True)
    email = models.EmailField()
    event_title = models.CharField(max_length=255)
    seatgeek_event_id = models.CharField(max_length=10)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
