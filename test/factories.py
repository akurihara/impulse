from __future__ import absolute_import

from decimal import Decimal

from alert.services import monitor_service
from event.lib.seatgeek_gateway import SeatGeekEvent, SeatGeekVenue
from event.models import Venue
from event.services import event_service
from test.fixtures import PURITY_RING_EVENT, PURITY_RING_SEATGEEK_EVENT, TERMINAL_5_VENUE, TERMINAL_5_SEATGEEK_VENUE

VALID_PHONE_NUMBER = '+15005550006'
PURITY_RING_EVENT_URL = 'https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'


def create_event(datetime_start=None):
    event_fixture = PURITY_RING_EVENT.copy()

    event_fixture['venue'] = create_venue()
    if datetime_start:
        event_fixture['datetime_start'] = datetime_start

    return event_service.create_event(**event_fixture)


def create_monitor_for_event(event, amount=None, phone_number=None, status=None):
    amount = amount or Decimal('65.01')
    phone_number = phone_number or VALID_PHONE_NUMBER

    monitor = monitor_service.create_monitor_for_event(
        event=event,
        phone_number=phone_number,
        amount=amount
    )

    if status:
        monitor_service.set_status_of_monitor(monitor, status)

    return monitor


def create_venue():
    venue_fixture = TERMINAL_5_VENUE.copy()

    return Venue.objects.create(**venue_fixture)


def create_seatgeek_event():
    seatgeek_venue = create_seatgeek_venue()
    seatgeek_event_fixture = PURITY_RING_SEATGEEK_EVENT.copy()
    seatgeek_event_fixture['venue'] = seatgeek_venue

    return SeatGeekEvent(**seatgeek_event_fixture)


def create_seatgeek_venue():
    return SeatGeekVenue(**TERMINAL_5_SEATGEEK_VENUE)
