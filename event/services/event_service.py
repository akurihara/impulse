from datetime import timedelta

from django.utils import timezone

from event.lib.seatgeek_gateway import search_upcoming_events
from event.models import Event, EventPrice, VENDOR_TYPE_SEATGEEK

__all__ = [
    'create_event',
    'create_event_price_for_event',
    'get_events_starting_in_next_twenty_four_hours',
    'find_or_create_upcoming_events_matching_query'
]


def create_event(vendor_id, vendor_type, title, datetime_start, price, url):
    event = Event.objects.create(
        datetime_start=datetime_start,
        title=title,
        url=url,
        vendor_id=vendor_id,
        vendor_type=vendor_type,
    )

    if price:
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


def find_or_create_upcoming_events_matching_query(query):
    seatgeek_events = search_upcoming_events(query)

    return [_find_or_create_event(seatgeek_event) for seatgeek_event in seatgeek_events]


def _find_or_create_event(seatgeek_event):
    try:
        event = Event.objects.get(
            vendor_id=seatgeek_event.id,
            vendor_type=VENDOR_TYPE_SEATGEEK
        )
    except Event.DoesNotExist:
        event = create_event(
            vendor_id=seatgeek_event.id,
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title=seatgeek_event.title,
            datetime_start=seatgeek_event.datetime_utc,
            price=seatgeek_event.lowest_price,
            url=seatgeek_event.url
        )

    return event
