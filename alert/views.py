import json
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from alert.services import monitor_service


class MonitorsHandler(View):

    def post(self, request):
        parameters = json.loads(request.body)
        seatgeek_event_id = parameters['seatgeek_event_id']
        phone_number = parameters['phone_number']
        amount = parameters['amount']

        monitor = monitor_service.create_monitor(
            seatgeek_event_id=seatgeek_event_id,
            phone_number=phone_number,
            amount = Decimal(amount)
        )

        return HttpResponse(status=201)
