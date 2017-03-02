from django import forms

from alert.services import monitor_service
from event.models import Event


class MonitorForm(forms.Form):
    amount = forms.DecimalField()
    phone_number = forms.CharField(max_length=100)
    event_id = forms.CharField(max_length=100)

    def clean_event_id(self):
        event_id = self.cleaned_data['event_id']
        event = Event.objects.get(id=event_id)
        self.cleaned_data['event'] = event

        return event_id

    def save(form):
        cleaned_data = form.cleaned_data

        return monitor_service.create_monitor_for_event(
            event=cleaned_data['event'],
            phone_number=cleaned_data['phone_number'],
            amount=cleaned_data['amount']
        )
