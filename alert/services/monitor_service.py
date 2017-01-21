from datetime import datetime, time, timedelta

from django.utils import timezone

from alert.models import Monitor
from lib import seatgeek_gateway


def create_monitor(seatgeek_event_id, phone_number, amount):
    event = seatgeek_gateway.get_event_by_id(seatgeek_event_id)

    return Monitor.objects.create(
        amount=amount,
        datetime_event_start=event.datetime_utc,
        event_title=event.title,
        phone_number=phone_number,
        seatgeek_event_id=seatgeek_event_id
    )


def get_monitors_for_events_in_next_twenty_four_hours():
    now = timezone.now()
    twenty_four_hours_from_now = now + timedelta(days=1)

    return Monitor.objects.filter(
        datetime_event_start__range=(now, twenty_four_hours_from_now)
    )
