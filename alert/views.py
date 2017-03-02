from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from alert.constants import (
    INCOMING_MESSAGE_ACTIVATE_MONITOR,
    INCOMING_MESSAGE_DEACTIVATE_MONITOR,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED
)
from alert.forms import MonitorForm
from alert.services import monitor_service


class CreateMonitorView(View):

    def post(self, request):
        amount = request.POST['amount']
        amount_as_decimal = Decimal(str(amount))
        event_id = request.POST['event_id']

        monitor_data = {
            'amount': amount_as_decimal,
            'phone_number': request.POST['phone_number'],
            'event_id': event_id
        }

        form = MonitorForm(monitor_data)
        if form.is_valid():
            monitor = form.save()

            redirect_url = '/events/{event_id}/monitors/{monitor_id}'.format(
                event_id=monitor.event.id,
                monitor_id=monitor.id
            )

            return HttpResponseRedirect(redirect_url)


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
