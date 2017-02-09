from datetime import datetime, time, timedelta
import os

from django.db.models import Max, Prefetch
from twilio.rest import TwilioRestClient

from alert.constants import (
    MONITOR_CONFIRMATION_MESSAGE,
    MONITOR_STATUSES,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_CREATED
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
    message = MONITOR_CONFIRMATION_MESSAGE.format(event_title=event_title)

    twilio_client.messages.create(body=message, to=monitor.phone_number.as_e164, from_=twilio_number)


def _load_twilio_config():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    return twilio_number, twilio_account_sid, twilio_auth_token


def _format_event_title(title):
    return (title[:60] + '...') if len(title) > 60 else title


def does_activated_or_created_monitor_exist_for_phone_number(phone_number):
    return Monitor.objects.annotate(
        most_recent_status=Max('statuses__status')
    ).filter(
        phone_number=phone_number,
        most_recent_status__in=(MONITOR_STATUS_ACTIVATED, MONITOR_STATUS_CREATED)
    ).exists()
