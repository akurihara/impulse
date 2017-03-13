from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

VENDOR_TYPE_SEATGEEK = 0

VENDOR_TYPES = {
    VENDOR_TYPE_SEATGEEK: 'Seatgeek'
}


class Event(models.Model):
    external_id = models.CharField(db_index=True, max_length=10)
    datetime_start = models.DateTimeField()
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    vendor_id = models.CharField(max_length=10)
    vendor_type = models.PositiveSmallIntegerField(choices=VENDOR_TYPES.items())

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.id})

    @property
    def current_price(self):
        return self.prices.latest()


class EventPrice(models.Model):

    class Meta:
        get_latest_by = 'id'

    event = models.ForeignKey('Event', related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)
