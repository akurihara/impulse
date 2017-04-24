from django.db.models import Max

from impulse.alert.constants import (
    MONITOR_STATUSES,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_CREATED,
    OUTGOING_MESSAGE_MONITOR_CONFIRMATION
)
from impulse.alert.lib.twilio_gateway import send_sms_message
from impulse.alert.models import Monitor, MonitorStatus
from impulse.utils import generate_external_id

__all__ = [
    'create_monitor_for_event',
    'set_status_of_monitor',
    'does_activated_or_created_monitor_exist_for_phone_number',
    'get_created_monitor_for_phone_number',
    'get_activated_monitor_for_phone_number'
]


def create_monitor_for_event(event, phone_number, amount):
    if does_activated_or_created_monitor_exist_for_phone_number(phone_number):
        raise ValueError('All monitors for {} have not been deactivated'.format(phone_number))

    monitor = Monitor.objects.create(
        amount=amount,
        phone_number=phone_number,
        event=event
    )

    monitor = _update_monitor_with_external_id(monitor)

    MonitorStatus.objects.create(
        monitor=monitor,
        status=MONITOR_STATUS_CREATED
    )

    _send_monitor_confirmation_message(monitor, event)

    return monitor


def _update_monitor_with_external_id(monitor):
    monitor.external_id = generate_external_id(monitor.id)
    monitor.save()

    return monitor


def _send_monitor_confirmation_message(monitor, event):
    event_title = _format_event_title(event.title)
    message = OUTGOING_MESSAGE_MONITOR_CONFIRMATION.format(event_title=event_title)

    send_sms_message(to_phone_number=monitor.phone_number.as_e164, message=message)


def set_status_of_monitor(monitor, status):
    if status not in MONITOR_STATUSES:
        raise ValueError('Status must be one of {}'.format(MONITOR_STATUSES))

    MonitorStatus.objects.create(
        monitor=monitor,
        status=status
    )


def _format_event_title(title):
    return (title[:60] + '...') if len(title) > 60 else title


def does_activated_or_created_monitor_exist_for_phone_number(phone_number):
    statuses = (MONITOR_STATUS_CREATED, MONITOR_STATUS_ACTIVATED)
    activated_or_created_monitors = _get_monitors_with_current_statuses_queryset(statuses)

    return activated_or_created_monitors.filter(
        phone_number=phone_number,
    ).exists()


def get_created_monitor_for_phone_number(phone_number):
    statuses = (MONITOR_STATUS_CREATED,)

    try:
        created_monitors = _get_monitors_with_current_statuses_queryset(statuses)
        monitor = created_monitors.get(phone_number=phone_number)
    except Monitor.DoesNotExist:
        monitor = None

    return monitor


def get_activated_monitor_for_phone_number(phone_number):
    statuses = (MONITOR_STATUS_ACTIVATED,)

    try:
        activated_monitors = _get_monitors_with_current_statuses_queryset(statuses)
        monitor = activated_monitors.get(phone_number=phone_number)
    except Monitor.DoesNotExist:
        monitor = None

    return monitor


def _get_monitors_with_current_statuses_queryset(statuses):
    return Monitor.objects.annotate(
        most_recent_status=Max('statuses__status')
    ).filter(
        most_recent_status__in=statuses
    )
