from datetime import datetime, timedelta
from decimal import Decimal
from mock import patch
import pytz

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from impulse.event.models import Event, VENDOR_TYPE_SEATGEEK, Venue
from impulse.event.services import event_service
from test import factories, fixtures


class CreateEventTest(TestCase):

    def test_creates_new_event(self):
        venue = factories.create_venue()
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            datetime_start_local=datetime(2017, 1, 19, 22, 0, tzinfo=pytz.utc),
            price=Decimal('65'),
            url=fixtures.PURITY_RING_EVENT_URL,
            venue=venue
        )

        self.assertTrue(Event.objects.filter(id=event.id).exists())
        self.assertEqual('3621831', event.vendor_id)
        self.assertEqual(VENDOR_TYPE_SEATGEEK, event.vendor_type)
        self.assertEqual('Purity Ring', event.title)
        self.assertEqual(fixtures.PURITY_RING_EVENT_URL, event.url)
        self.assertEqual(datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc), event.datetime_start)
        self.assertEqual(venue.id, event.venue_id)
        self.assertRegexpMatches(event.external_id, '^[a-z]{5,10}$')

    def test_creates_event_price_for_event(self):
        venue = factories.create_venue()
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            datetime_start_local=datetime(2017, 1, 19, 22, 0, tzinfo=pytz.utc),
            price=Decimal('65'),
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831',
            venue=venue
        )

        self.assertEqual(1, event.prices.count())
        self.assertEqual(Decimal('65'), event.current_price.price)

    def test_does_not_create_event_price_for_event_if_price_is_none(self):
        venue = factories.create_venue()
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            datetime_start_local=datetime(2017, 1, 19, 22, 0, tzinfo=pytz.utc),
            price=None,
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831',
            venue=venue
        )

        self.assertEqual(0, event.prices.count())


class CreateEventPriceForEventTest(TestCase):

    def test_creates_new_event_price(self):
        event = factories.create_event()

        event_service.create_event_price_for_event(event, Decimal('60'))

        self.assertEqual(2, event.prices.count())
        self.assertEqual(Decimal('60'), event.current_price.price)


class GetEventsStartingInNextTwentyFourHoursTest(TestCase):

    def test_returns_event_with_event_starting_now(self):
        now = timezone.now()
        event = factories.create_event(datetime_start=now)

        with freeze_time(now):
            events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(1, len(events))
        self.assertIn(event, events)

    def test_returns_event_starting_in_less_than_twenty_four_hours(self):
        twenty_three_hours_from_now = timezone.now() + timedelta(hours=23)
        event = factories.create_event(datetime_start=twenty_three_hours_from_now)

        events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(1, len(events))
        self.assertIn(event, events)

    def test_does_not_return_monitor_for_past_event(self):
        one_second_ago = timezone.now() - timedelta(seconds=1)
        factories.create_event(datetime_start=one_second_ago)

        events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(0, len(events))

    def test_does_not_return_monitor_for_event_more_than_twenty_four_hours_from_now(self):
        twenty_five_hours_from_now = timezone.now() + timedelta(hours=25)
        factories.create_event(datetime_start=twenty_five_hours_from_now)

        events = event_service.get_events_starting_in_next_twenty_four_hours()

        self.assertEqual(0, len(events))


class FindOrCreateUpcomingEventsMatchingQueryTest(TestCase):

    def test_creates_event_if_event_does_not_exist_with_seatgeek_event_id(self):
        mock_seatgeek_event = factories.create_seatgeek_event()

        with patch('impulse.event.services.event_service.search_upcoming_events', return_value=[mock_seatgeek_event]):
            upcoming_events = event_service.find_or_create_upcoming_events_matching_query('query')

        self.assertEqual(1, len(upcoming_events))
        self.assertTrue(Event.objects.filter(vendor_id=mock_seatgeek_event.id).exists())

    def test_returns_existing_event_that_has_seatgeek_event_id(self):
        event = factories.create_event()
        mock_seatgeek_event = factories.create_seatgeek_event()

        with patch('impulse.event.services.event_service.search_upcoming_events', return_value=[mock_seatgeek_event]):
            upcoming_events = event_service.find_or_create_upcoming_events_matching_query('query')

        self.assertEqual(1, len(upcoming_events))
        self.assertEqual(event.id, upcoming_events[0].id)


class FindOrCreateVenueTest(TestCase):

    def test_creates_venue_if_venue_does_not_exist_with_seatgeek_venue_id(self):
        mock_seatgeek_venue = factories.create_seatgeek_venue()

        event_service.find_or_create_venue(mock_seatgeek_venue)

        self.assertTrue(Venue.objects.filter(vendor_id=mock_seatgeek_venue.id).exists())

    def test_returns_existing_venue_that_has_seatgeek_venue_id(self):
        existing_venue = factories.create_venue()
        mock_seatgeek_venue = factories.create_seatgeek_venue()

        actual_venue = event_service.find_or_create_venue(mock_seatgeek_venue)

        self.assertTrue(existing_venue.id, actual_venue.id)
