import django
django.setup()

from django.utils import timezone

from impulse.alert.constants import (
    MONITOR_STATUS_CREATED,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED,
    OUTGOING_MESSAGE_MONITOR_TRIGGERED
)
from impulse.alert.lib.twilio_gateway import send_sms_message
from impulse.alert.services import monitor_service
from impulse.event.lib.seatgeek_gateway import get_event_by_id
from impulse.event.services.event_service import (
    get_events_starting_in_next_twenty_four_hours,
    create_event_price_for_event
)


def main():
    events = get_events_starting_in_next_twenty_four_hours()

    for event in events:
        _update_event_with_latest_price(event)
        _check_for_triggered_monitors_and_send_alerts(event)
        _deactivate_monitors_if_event_starts_in_next_hour(event)


def _update_event_with_latest_price(event):
    seatgeek_event = get_event_by_id(event.vendor_id)

    if seatgeek_event.lowest_price:
        create_event_price_for_event(event, seatgeek_event.lowest_price)


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


def _deactivate_monitors_if_event_starts_in_next_hour(event):
    now = timezone.now()
    seconds_until_event_starts = (event.datetime_start - now).seconds
    one_hour_in_seconds = 60 * 60

    if seconds_until_event_starts < one_hour_in_seconds:
        for monitor in event.monitors.all():
            if monitor.current_status.status in [MONITOR_STATUS_ACTIVATED, MONITOR_STATUS_CREATED]:
                monitor_service.set_status_of_monitor(
                    monitor=monitor,
                    status=MONITOR_STATUS_DEACTIVATED
                )


if __name__ == "__main__":
    main()
