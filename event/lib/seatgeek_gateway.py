import os
from collections import namedtuple
import datetime
from decimal import Decimal
import json
import pytz

from django.utils import timezone
import requests

SEATGEEK_BASE_URL = 'https://api.seatgeek.com/2/'
SEATGEEK_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
SEATGEEK_CLIENT_ID = os.environ.get('SEATGEEK_CLIENT_ID')
SEATGEEK_CLIENT_SECRET = os.environ.get('SEATGEEK_CLIENT_SECRET')

SeatGeekEvent = namedtuple(
    'SeatGeekEvent',
    ['id', 'title', 'datetime_utc', 'lowest_price', 'url', 'venue']
)

SeatGeekVenue = namedtuple(
    'SeatGeekVenue',
    ['id', 'name', 'city', 'state', 'country']
)


def get_event_by_id(event_id):
    url = '{base}/events/{event_id}'.format(
        base=SEATGEEK_BASE_URL,
        event_id=event_id
    )
    response = requests.get(url, auth=(SEATGEEK_CLIENT_ID, SEATGEEK_CLIENT_SECRET))
    event_data = json.loads(response.text)

    if response.status_code != 200:
        _handle_error_response(response)

    return _get_seatgeek_event_tuple_from_event_data(event_data)


def _get_seatgeek_event_tuple_from_event_data(event_data):
    datetime_utc = datetime.datetime.strptime(event_data['datetime_utc'], SEATGEEK_DATETIME_FORMAT)
    localized_datetime_utc = pytz.utc.localize(datetime_utc)
    lowest_price = _get_lowest_price_from_event_data(event_data)
    seatgeek_venue = _get_seatgeek_venue_from_seatgeek_event(event_data)

    return SeatGeekEvent(
        id=event_data['id'],
        title=event_data['short_title'],
        datetime_utc=localized_datetime_utc,
        lowest_price=lowest_price,
        url=event_data['url'],
        venue=seatgeek_venue
    )


def _get_lowest_price_from_event_data(event_data):
    lowest_price = event_data['stats']['lowest_price']

    return Decimal(lowest_price) if lowest_price else None


def _get_seatgeek_venue_from_seatgeek_event(seatgeek_event):
    venue_data = seatgeek_event['venue']

    return SeatGeekVenue(
        id=venue_data['id'],
        name=venue_data['name'],
        city=venue_data['city'],
        state=venue_data['state'],
        country=venue_data['country']
    )


def search_upcoming_events(query):
    url = '{base}/events'.format(base=SEATGEEK_BASE_URL)
    parameters = {
        'datetime_utc.gte': timezone.now().strftime(SEATGEEK_DATETIME_FORMAT),
        'q': query
    }
    response = requests.get(
        url=url,
        auth=(SEATGEEK_CLIENT_ID, SEATGEEK_CLIENT_SECRET),
        params=parameters
    )

    if response.status_code != 200:
        _handle_error_response(response)

    events_data = json.loads(response.text)

    return [_get_seatgeek_event_tuple_from_event_data(event_data) for event_data in events_data['events']]


def _handle_error_response(response):
    message = 'Seatgeek API responded with {}'.format(response.status_code)
    raise RuntimeError(message)
