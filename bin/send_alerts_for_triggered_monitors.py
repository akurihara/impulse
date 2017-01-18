import os

from twilio.rest import TwilioRestClient

from alert.services import monitor_service
from lib.seatgeek_gateway import get_event_by_id


def main():
    monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

    for monitor in monitors:
        event = get_event_by_id(monitor.seatgeek_event_id)
        if event.lowest_price <= monitor.amount:
            _send_alert_to_user(event)


def _send_alert_to_user(event):
    twilio_number, twilio_account_sid, twilio_auth_token = _load_twilio_config()
    twilio_client = TwilioRestClient(twilio_account_sid, twilio_auth_token)
    message = 'Lowest price for {event_name} is ${amount}'.format(
        event_name=event.title,
        amount=event.lowest_price
    )

    twilio_client.messages.create(body=message, to='+13106172186', from_=twilio_number)


def _load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    return twilio_number, twilio_account_sid, twilio_auth_token


if __name__ == "__main__":
    main()
