import json
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from alert.constants import (
    INCOMING_MESSAGE_ACTIVATE_MONITOR,
    INCOMING_MESSAGE_DEACTIVATE_MONITOR
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

        monitor = monitor_service.create_monitor_for_event(
            event_id=event_id,
            phone_number=phone_number,
            amount = Decimal(amount)
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

        if message == INCOMING_MESSAGE_ACTIVATE_MONITOR:
            monitor = get_created_monitor_for_phone_number(phone_number)
            if monitor:
                monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)
        elif message == INCOMING_MESSAGE_DEACTIVATE_MONITOR:
            monitor = get_activated_monitor_for_phone_number(phone_number)
            if monitor:
                monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)

        return HttpResponse(status=200)
