from datetime import datetime, time, timedelta

from alert.constants import MONITOR_STATUSES, MONITOR_STATUS_CREATED
from alert.models import Monitor, MonitorStatus


def create_monitor_for_event(event, phone_number, amount):
    monitor = Monitor.objects.create(
        amount=amount,
        phone_number=phone_number,
        event=event
    )
    MonitorStatus.objects.create(
        monitor=monitor,
        status=MONITOR_STATUS_CREATED
    )

    return monitor


def set_status_of_monitor(monitor, status):
    if status not in MONITOR_STATUSES:
        raise ValueError('Status must be one of {}'.format(MONITOR_STATUSES))

    MonitorStatus.objects.create(
        monitor=monitor,
        status=status
    )
