from datetime import datetime, time, timedelta

from django.utils import timezone

from alert.models import Monitor
from event.lib import seatgeek_gateway


def create_monitor(seatgeek_event_id, phone_number, amount):
    event = seatgeek_gateway.get_event_by_id(seatgeek_event_id)

    return Monitor.objects.create(
        amount=amount,
        datetime_event_start=event.datetime_utc,
        event_title=event.title,
        phone_number=phone_number,
        seatgeek_event_id=seatgeek_event_id
    )
