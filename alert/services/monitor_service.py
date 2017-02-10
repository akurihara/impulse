import os

from django.db.models import Max
from twilio.rest import TwilioRestClient

from alert.constants import (
    MONITOR_STATUSES,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_CREATED,
    OUTGOING_MESSAGE_MONITOR_CONFIRMATION
)
from alert.models import Monitor, MonitorStatus


def create_monitor_for_event(event, phone_number, amount):
    if does_activated_or_created_monitor_exist_for_phone_number(phone_number):
        raise ValueError('All monitors for {} have not been deactivated'.format(phone_number))

    monitor = Monitor.objects.create(
        amount=amount,
        phone_number=phone_number,
        event=event
    )
    MonitorStatus.objects.create(
        monitor=monitor,
        status=MONITOR_STATUS_CREATED
    )

    _send_monitor_confirmation_message(monitor, event)

    return monitor


def set_status_of_monitor(monitor, status):
    if status not in MONITOR_STATUSES:
        raise ValueError('Status must be one of {}'.format(MONITOR_STATUSES))

    MonitorStatus.objects.create(
        monitor=monitor,
        status=status
    )


def _send_monitor_confirmation_message(monitor, event):
    twilio_number, twilio_account_sid, twilio_auth_token = _load_twilio_config()
    twilio_client = TwilioRestClient(twilio_account_sid, twilio_auth_token)

    event_title = _format_event_title(event.title)
    message = OUTGOING_MESSAGE_MONITOR_CONFIRMATION.format(event_title=event_title)

    twilio_client.messages.create(body=message, to=monitor.phone_number.as_e164, from_=twilio_number)


def _load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    return twilio_number, twilio_account_sid, twilio_auth_token


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
