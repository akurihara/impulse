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
    datetime_start_local = models.DateTimeField()
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    vendor_id = models.CharField(max_length=10)
    vendor_type = models.PositiveSmallIntegerField(choices=VENDOR_TYPES.items())
    venue = models.ForeignKey('Venue', related_name='events', null=True)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk': self.id})

    @property
    def current_price(self):
        return self.prices.latest()

    @property
    def display_title(self):
        if len(self.title) > 40:
            display_title = self.title[:40] + '...'
        else:
            display_title = self.title

        return display_title


class EventPrice(models.Model):

    class Meta:
        get_latest_by = 'id'

    event = models.ForeignKey('Event', related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)


class Venue(models.Model):

    class Meta:
        get_latest_by = 'id'

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True)
    state = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    vendor_id = models.CharField(max_length=10)
    vendor_type = models.PositiveSmallIntegerField(choices=VENDOR_TYPES.items())

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)
