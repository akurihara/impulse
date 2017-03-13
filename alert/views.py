from decimal import Decimal
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from alert.constants import (
    INCOMING_MESSAGE_ACTIVATE_MONITOR,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED,
    VALID_INCOMING_MESSAGES
)
from alert.forms import MonitorForm
from alert.lib.twilio_gateway import create_twiml_response
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

            redirect_url = '/events/{event_external_id}/monitors/{monitor_external_id}'.format(
                event_id=monitor.event.external_id,
                monitor_id=monitor.external_id
            )

            return HttpResponseRedirect(redirect_url)


class IncomingSMSMessageView(View):

    def post(self, request):
        phone_number = request.POST['From']
        incoming_message = request.POST['Body'].strip()

        if incoming_message not in VALID_INCOMING_MESSAGES:
            return HttpResponse(status=200)

        monitor = monitor_service.get_created_monitor_for_phone_number(phone_number)

        if not monitor:
            return HttpResponse(status=200)

        _update_monitor_status_from_incoming_message(monitor, incoming_message)
        outgoing_message = _get_outgoing_message_from_incoming_message(monitor, incoming_message)
        twiml_response = create_twiml_response(outgoing_message)

        return HttpResponse(str(twiml_response), status=200)


def _update_monitor_status_from_incoming_message(monitor, incoming_message):
    if incoming_message == INCOMING_MESSAGE_ACTIVATE_MONITOR:
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)
    else:
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)


def _get_outgoing_message_from_incoming_message(monitor, incoming_message):
    if incoming_message == INCOMING_MESSAGE_ACTIVATE_MONITOR:
        outgoing_message = 'Your price tracker has been activated.'
    else:
        outgoing_message = 'You have canceled the price tracker for this number.'

    return outgoing_message
