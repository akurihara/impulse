from django.forms import ModelForm

from alert.models import Monitor
from alert.services import monitor_service


class MonitorForm(ModelForm):

    class Meta:
        model = Monitor
        fields = ['amount', 'phone_number', 'seatgeek_event_id']

    def save(form):
        cleaned_data = form.cleaned_data

        monitor = monitor_service.create_monitor(
            seatgeek_event_id=cleaned_data['seatgeek_event_id'],
            phone_number=cleaned_data['phone_number'],
            amount=cleaned_data['amount']
        )
