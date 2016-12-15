from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from alert.models import Monitor
from alert.services import monitor_service


class CreateMonitorTest(TestCase):

    def test_creates_new_monitor(self):
        monitor = monitor_service.create_monitor(
            seatgeek_event_id='3575009',
            email='alex.kurihara@gmail.com',
            amount=Decimal('1')
        )

        self.assertTrue(Monitor.objects.filter(id=monitor.id).exists())
        self.assertEqual('3575009', monitor.seatgeek_event_id)
        self.assertEqual('alex.kurihara@gmail.com', monitor.email)
        self.assertEqual(Decimal('1'), monitor.amount)


class GetMonitorsForEventsStartingInNextTwentyFourHoursTest(TestCase):

    def test_returns_monitor_with_event_starting_now(self):
        monitor = Monitor.objects.create(
            amount=Decimal('1'),
            datetime_event_start=timezone.now(),
            event_title='foo',
            email='foo@bar.com',
            seatgeek_event_id='123'
        )

        monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

        self.assertEqual(1, len(monitors))
        self.assertIn(monitor, monitors)

    def test_returns_monitor_for_event_starting_in_less_than_twenty_four_hours(self):
        twenty_three_hours_from_now = timezone.now() + timedelta(hours=23)

        monitor = Monitor.objects.create(
            amount=Decimal('1'),
            datetime_event_start=twenty_three_hours_from_now,
            event_title='foo',
            email='foo@bar.com',
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
            email='foo@bar.com',
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
            email='foo@bar.com',
            seatgeek_event_id='123'
        )

        monitors = monitor_service.get_monitors_for_events_in_next_twenty_four_hours()

        self.assertEqual(0, len(monitors))
