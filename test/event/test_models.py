from datetime import datetime
from decimal import Decimal
import pytz

from django.test import TestCase

from event.models import Event, EventPrice, VENDOR_TYPE_SEATGEEK
from event.services import event_service


class CurrentEventPriceTest(TestCase):

    def test_returns_latest_event_price(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65')
        )
        event_service.create_event_price_for_event(event, Decimal('60'))

        current_event_price = event.current_event_price

        self.assertEqual(EventPrice.objects.filter(event=event).latest(), current_event_price)
