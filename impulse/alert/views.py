from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from django.views import View

from impulse.alert.constants import (
    INCOMING_MESSAGE_ACTIVATE_MONITOR,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED,
    VALID_INCOMING_MESSAGES
)
from impulse.alert.forms import MonitorForm
from impulse.alert.lib.twilio_gateway import create_twiml_response
from impulse.alert.services import monitor_service
from impulse.event.models import Event


class CreateMonitorView(View):

    def post(self, request, event_external_id):
        event = Event.objects.get(external_id=event_external_id)
        monitor_data = {
            'amount': request.POST['amount'],
            'phone_number': request.POST['phone_number'],
            'event': event.id
        }

        form = MonitorForm(monitor_data)

        if form.is_valid():
            monitor = form.save()

            redirect_url = '/events/{event_external_id}/monitors/{monitor_external_id}'.format(
                event_external_id=monitor.event.external_id,
                monitor_external_id=monitor.external_id
            )

            http_response = HttpResponseRedirect(redirect_url)
        else:
            template = loader.get_template('event/event_detail.html')
            context = RequestContext(
                request=request,
                dict_={'event': event, 'errors': form.errors}
            )

            http_response = HttpResponse(template.render(context))

        return http_response


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
