from __future__ import unicode_literals

from django.db import models

VENDOR_TYPE_SEATGEEK = 0

VENDOR_TYPES = {
    VENDOR_TYPE_SEATGEEK: 'Seatgeek'
}


class Event(models.Model):
    datetime_start = models.DateTimeField()
    title = models.CharField(max_length=255)
    vendor_id = models.CharField(max_length=10)
    vendor_type = models.PositiveSmallIntegerField(choices=VENDOR_TYPES.items())

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)


class EventPrice(models.Model):
    event = models.ForeignKey('Event')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
