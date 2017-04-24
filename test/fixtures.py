from __future__ import absolute_import

from datetime import datetime
from decimal import Decimal
import pytz

from impulse.event.models import VENDOR_TYPE_SEATGEEK

PURITY_RING_EVENT_URL = 'https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'

PURITY_RING_EVENT = {
    'datetime_start': datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
    'price': Decimal('65'),
    'url': PURITY_RING_EVENT_URL,
    'title': 'Purity Ring',
    'vendor_id': '3621831',
    'vendor_type': VENDOR_TYPE_SEATGEEK,
    'venue': None
}

TERMINAL_5_VENUE = {
    'name': 'Terminal 5',
    'city': 'New York',
    'state': 'NY',
    'country': 'US',
    'vendor_id': '814',
    'vendor_type': VENDOR_TYPE_SEATGEEK,
}

TERMINAL_5_SEATGEEK_VENUE = {
    'id': '814',
    'name': 'Terminal 5',
    'city': 'New York',
    'state': 'NY',
    'country': 'US',
}

PURITY_RING_SEATGEEK_EVENT = {
    'id': '3621831',
    'datetime_utc': datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
    'lowest_price': Decimal('65'),
    'title': 'Purity Ring',
    'url': PURITY_RING_EVENT_URL,
    'venue': None
}
