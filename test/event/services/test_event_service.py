from datetime import datetime
from decimal import Decimal
import pytz

from django.test import TestCase

from event.models import Event, EventPrice, VENDOR_TYPE_SEATGEEK
from event.services import event_service


class CreateEventTest(TestCase):

    def test_creates_new_event(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65')
        )

        self.assertTrue(Event.objects.filter(id=event.id).exists())

    def test_creates_event_price_for_event(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65')
        )

        self.assertEqual(1, EventPrice.objects.filter(event_id=event.id).count())


class CreateEventPriceForEventTest(TestCase):

    def test_creates_new_event_price(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65')
        )

        event_service.create_event_price_for_event(event, Decimal('60'))

        self.assertEqual(2, EventPrice.objects.filter(event_id=event.id).count())
