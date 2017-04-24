import django
django.setup()

from impulse.alert.constants import (
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED,
    OUTGOING_MESSAGE_MONITOR_TRIGGERED
)
from impulse.alert.lib.twilio_gateway import send_sms_message
from impulse.alert.services import monitor_service
from impulse.event.lib.seatgeek_gateway import get_event_by_id
from impulse.event.services import event_service


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
            _send_alert_message_to_user(event, monitor)
            monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)


def _should_send_alert_to_user(event, monitor):
    return (
        event.current_price.price <= monitor.amount and
        monitor.current_status.status == MONITOR_STATUS_ACTIVATED
    )


def _send_alert_message_to_user(event, monitor):
    message = OUTGOING_MESSAGE_MONITOR_TRIGGERED.format(
        event_title=event.title,
        amount=event.current_price.price,
        url=event.url
    )
    send_sms_message(to_phone_number=monitor.phone_number.as_e164, message=message)


if __name__ == "__main__":
    main()
