from datetime import timedelta

from django.utils import timezone

from event.models import Event, EventPrice


def create_event(vendor_id, vendor_type, title, datetime_start, price, url):
    event = Event.objects.create(
        datetime_start=datetime_start,
        title=title,
        url=url,
        vendor_id=vendor_id,
        vendor_type=vendor_type,
    )
    create_event_price_for_event(event, price)

    return event


def create_event_price_for_event(event, price):
    EventPrice.objects.create(
        event=event,
        price=price
    )


def get_events_starting_in_next_twenty_four_hours():
    now = timezone.now()
    twenty_four_hours_from_now = now + timedelta(days=1)

    return Event.objects.filter(
        datetime_start__range=(now, twenty_four_hours_from_now)
    )
