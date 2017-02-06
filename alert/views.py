import json
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

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
        print '[{file_name}]: {request_body}'.format(
            file_name=__name__,
            request_body=request.body
        )
        print '[{file_name}]: {request_body}'.format(
            file_name=__name__,
            request_body=request.POST
        )

        return HttpResponse(status=200)
