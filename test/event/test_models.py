from datetime import datetime
from decimal import Decimal
import pytz

from django.test import TestCase

from event.models import Event, EventPrice, VENDOR_TYPE_SEATGEEK
from event.services import event_service
from test import factories


class CurrentEventPriceTest(TestCase):

    def test_returns_latest_event_price(self):
        event = factories.create_event()
        event_service.create_event_price_for_event(event, Decimal('60'))

        current_event_price = event.current_event_price

        self.assertEqual(EventPrice.objects.filter(event=event).latest(), current_event_price)
