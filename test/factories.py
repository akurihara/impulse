from __future__ import absolute_import

from datetime import datetime
from decimal import Decimal
import pytz

from alert.services import monitor_service
from event.models import Event, VENDOR_TYPE_SEATGEEK
from event.services import event_service

VALID_PHONE_NUMBER = '+15005550006'


def create_event(datetime_start=None):
    datetime_start = datetime_start or datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc)

    return event_service.create_event(
        vendor_id='3621831',
        vendor_type=VENDOR_TYPE_SEATGEEK,
        title='Purity Ring',
        datetime_start=datetime_start,
        price=Decimal('65'),
        url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
    )


def create_monitor_for_event(event, amount=None, status=None):
    amount = amount or Decimal('65.01')

    monitor = monitor_service.create_monitor_for_event(
        event=event,
        phone_number=VALID_PHONE_NUMBER,
        amount=amount
    )

    if status:
        monitor_service.set_status_of_monitor(monitor, status)

    return monitor
