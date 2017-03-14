from django import forms
from django.core.exceptions import ValidationError
from phonenumbers import (
    format_number,
    is_valid_number,
    parse,
    PhoneNumberFormat
)

from alert.services import monitor_service
from event.models import Event


class MonitorForm(forms.Form):
    amount = forms.DecimalField()
    phone_number = forms.CharField(max_length=100)
    event = forms.ModelChoiceField(queryset=Event.objects.all())

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        parsed_phone_number = parse(phone_number, 'US')

        if not is_valid_number(parsed_phone_number):
            raise ValidationError('Enter a valid phone number.')

        return format_number(parsed_phone_number, PhoneNumberFormat.E164)

    def save(form):
        cleaned_data = form.cleaned_data

        return monitor_service.create_monitor_for_event(
            event=cleaned_data['event'],
            phone_number=cleaned_data['phone_number'],
            amount=cleaned_data['amount']
        )
