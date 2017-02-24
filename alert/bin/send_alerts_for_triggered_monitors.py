import os

import django
django.setup()
from twilio.rest import TwilioRestClient

from alert.constants import MONITOR_STATUS_ACTIVATED, OUTGOING_MESSAGE_MONITOR_TRIGGERED
from event.lib.seatgeek_gateway import get_event_by_id
from event.services import event_service


def main():
    events = event_service.get_events_starting_in_next_twenty_four_hours()

    for event in events:
        seatgeek_event = get_event_by_id(event.vendor_id)

        if not seatgeek_event.lowest_price:
            continue

        event_service.create_event_price_for_event(event, seatgeek_event.lowest_price)

        _check_for_triggered_monitors_and_send_alerts(event)


def _check_for_triggered_monitors_and_send_alerts(event):
    for monitor in event.monitors.all():
        if _should_send_alert_to_user(event, monitor):
            _send_alert_to_user(event, monitor)


def _should_send_alert_to_user(event, monitor):
    return (
        event.current_price.price <= monitor.amount and
        monitor.current_status.status == MONITOR_STATUS_ACTIVATED
    )


def _send_alert_to_user(event, monitor):
    twilio_number, twilio_account_sid, twilio_auth_token = _load_twilio_config()
    twilio_client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    message = OUTGOING_MESSAGE_MONITOR_TRIGGERED.format(
        event_title=event.title,
        amount=event.current_price.price,
        url=event.url
    )

    twilio_client.messages.create(body=message, to=monitor.phone_number.as_e164, from_=twilio_number)


def _load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    return twilio_number, twilio_account_sid, twilio_auth_token


if __name__ == "__main__":
    main()
