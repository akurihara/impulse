from django.db import models
from django.db.models import Max
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from impulse.alert.constants import MONITOR_STATUSES


class Monitor(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    external_id = models.CharField(db_index=True, max_length=10)
    phone_number = PhoneNumberField()
    event = models.ForeignKey('event.Event', null=True, related_name='monitors')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse('monitor-detail', kwargs={'pk': self.id})

    @classmethod
    def filter_statuses(cls, statuses):
        return cls.objects.annotate(
            most_recent_status=Max('statuses__status')
        ).filter(
            most_recent_status__in=statuses
        )

    @property
    def current_status(self):
        return self.statuses.latest()


class MonitorStatus(models.Model):

    class Meta:
        get_latest_by = 'id'

    monitor = models.ForeignKey('Monitor', related_name='statuses')
    status = models.PositiveSmallIntegerField(choices=MONITOR_STATUSES.items())

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id)
