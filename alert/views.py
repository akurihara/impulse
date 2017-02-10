import json
from decimal import Decimal

from django.http import HttpResponse
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from alert.constants import (
    INCOMING_MESSAGE_ACTIVATE_MONITOR,
    INCOMING_MESSAGE_DEACTIVATE_MONITOR,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED
)
from alert.forms import MonitorForm
from alert.models import Monitor
from alert.services import monitor_service


class MonitorsHandler(View):

    def post(self, request):
        parameters = json.loads(request.body)
        event_id = parameters['event_id']
        phone_number = parameters['phone_number']
        amount = parameters['amount']

        monitor_service.create_monitor_for_event(
            event_id=event_id,
            phone_number=phone_number,
            amount=Decimal(amount)
        )

        return HttpResponse(status=201)


class CreateMonitorView(CreateView):
    form_class = MonitorForm
    model = Monitor


class MonitorDetailView(DetailView):
    model = Monitor


class IncomingSMSMessageView(View):

    def post(self, request):
        phone_number = request.POST['From']
        message = request.POST['Body'].strip()
        monitor = monitor_service.get_created_monitor_for_phone_number(phone_number)

        if monitor:
            _update_monitor_status_from_message(monitor, message)

        return HttpResponse(status=200)


def _update_monitor_status_from_message(monitor, message):
    if message == INCOMING_MESSAGE_ACTIVATE_MONITOR:
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)
    elif message == INCOMING_MESSAGE_DEACTIVATE_MONITOR:
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)
