from datetime import datetime, timedelta
from decimal import Decimal
import pytz

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

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


class GetEventsStartingInNextTwentyFourHoursTest(TestCase):

    def test_returns_event_with_event_starting_now(self):
        now = timezone.now()
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=now,
            price=Decimal('65')
        )
        with freeze_time(now):
            events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(1, len(events))
        self.assertIn(event, events)

    def test_returns_event_starting_in_less_than_twenty_four_hours(self):
        twenty_three_hours_from_now = timezone.now() + timedelta(hours=23)
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=twenty_three_hours_from_now,
            price=Decimal('65')
        )

        events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(1, len(events))
        self.assertIn(event, events)

    def test_does_not_return_monitor_for_past_event(self):
        one_second_ago = timezone.now() - timedelta(seconds=1)
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=one_second_ago,
            price=Decimal('65')
        )

        events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(0, len(events))

    def test_does_not_return_monitor_for_event_more_than_twenty_four_hours_from_now(self):
        twenty_five_hours_from_now = timezone.now() + timedelta(hours=25)
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=twenty_five_hours_from_now,
            price=Decimal('65')
        )

        events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(0, len(events))
