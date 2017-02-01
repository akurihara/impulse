from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Monitor(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = PhoneNumberField()
    event = models.ForeignKey('event.Event', null=True, related_name='monitors')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('monitor-detail', kwargs={'pk': self.id})
