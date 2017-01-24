from datetime import datetime, timedelta
from decimal import Decimal
from mock import patch
import pytz

from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from alert.models import Monitor
from alert.services import monitor_service
from lib.seatgeek_gateway import Event


class CreateMonitorTest(TestCase):

    def test_creates_new_monitor(self):
        mock_event_datetime_start = datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc)
        mock_event = Event(
            id='3621831',
            title='Purity Ring',
            datetime_utc=mock_event_datetime_start,
            lowest_price=Decimal('65'),
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
        )

        with patch('lib.seatgeek_gateway.get_event_by_id', return_value=mock_event):
            monitor = monitor_service.create_monitor(
                seatgeek_event_id='3621831',
                phone_number='+12223334444',
                amount=Decimal('70')
            )

        self.assertTrue(Monitor.objects.filter(id=monitor.id).exists())
        self.assertEqual(Decimal('70'), monitor.amount)
        self.assertEqual(mock_event_datetime_start, monitor.datetime_event_start)
        self.assertEqual('+12223334444', monitor.phone_number.as_e164)
        self.assertEqual('Purity Ring', monitor.event_title)
        self.assertEqual('3621831', monitor.seatgeek_event_id)


class GetMonitorsForEventsStartingInNextTwentyFourHoursTest(TestCase):

    def test_returns_monitor_with_event_starting_now(self):
        now = timezone.now()
        monitor = Monitor.objects.create(
            amount=Decimal('1'),
            datetime_event_start=now,
            event_title='foo',
            phone_number='+12223334444',
            seatgeek_event_id='123'
        )
        with freeze_time(now):
            monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

        self.assertEqual(1, len(monitors))
        self.assertIn(monitor, monitors)

    def test_returns_monitor_for_event_starting_in_less_than_twenty_four_hours(self):
        twenty_three_hours_from_now = timezone.now() + timedelta(hours=23)

        monitor = Monitor.objects.create(
            amount=Decimal('1'),
            datetime_event_start=twenty_three_hours_from_now,
            event_title='foo',
            phone_number='+12223334444',
            seatgeek_event_id='123'
        )

        monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

        self.assertEqual(1, len(monitors))
        self.assertIn(monitor, monitors)

    def test_does_not_return_monitor_for_past_event(self):
        one_second_ago = timezone.now() - timedelta(seconds=1)

        monitor = Monitor.objects.create(
            amount=Decimal('1'),
            datetime_event_start=one_second_ago,
            event_title='foo',
            phone_number='+12223334444',
            seatgeek_event_id='123'
        )

        monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

        self.assertEqual(0, len(monitors))

    def test_does_not_return_monitor_for_event_more_than_twenty_four_hours_from_now(self):
        twenty_five_hours_from_now = timezone.now() + timedelta(hours=25)

        monitor = Monitor.objects.create(
            amount=Decimal('1'),
            datetime_event_start=twenty_five_hours_from_now,
            event_title='foo',
            phone_number='+12223334444',
            seatgeek_event_id='123'
        )

        monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

        self.assertEqual(0, len(monitors))
