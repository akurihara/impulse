import os
from collections import namedtuple
import datetime
from decimal import Decimal
import json

import requests

SEATGEEK_BASE_URL = 'https://api.seatgeek.com/2/'
SEATGEEK_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'
SEATGEEK_CLIENT_ID = os.environ.get('SEATGEEK_CLIENT_ID')
SEATGEEK_CLIENT_SECRET = os.environ.get('SEATGEEK_CLIENT_SECRET')

Event = namedtuple('Event', ['id', 'title', 'datetime_utc', 'lowest_price'])


def get_event_by_id(event_id):
    url = '{base}/events/{event_id}'.format(
        base=SEATGEEK_BASE_URL,
        event_id=event_id
    )
    response = requests.get(url, auth=(SEATGEEK_CLIENT_ID, SEATGEEK_CLIENT_SECRET))
    event_data = json.loads(response.text)

    if response.status_code != 200:
        _handle_error_response(response)


    return _get_event_tuple_from_event_data(event_data)


def _get_event_tuple_from_event_data(event_data):
    datetime_utc = datetime.datetime.strptime(event_data['datetime_utc'], SEATGEEK_DATETIME_FORMAT)
    lowest_price_in_cents = Decimal(event_data['stats']['lowest_price'])
    lowest_price = lowest_price_in_cents / 100

    return Event(
        id=event_data['id'],
        title=event_data['short_title'],
        datetime_utc=datetime_utc,
        lowest_price=lowest_price
    )


def _handle_error_response(response):
    message = 'Seatgeek API responded with {}'.format(response.status_code)
    raise RuntimeError(message)
