from datetime import datetime
from decimal import Decimal
import pytz

from django.test import TestCase

from alert.constants import MONITOR_STATUS_ACTIVATED, MONITOR_STATUS_CREATED
from alert.models import Monitor, MonitorStatus
from alert.services import monitor_service
from event.models import VENDOR_TYPE_SEATGEEK
from event.services import event_service


class CreateMonitorForEventTest(TestCase):

    def test_creates_new_monitor(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65'),
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
        )

        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('70')
        )

        self.assertTrue(Monitor.objects.filter(id=monitor.id).exists())
        self.assertEqual(Decimal('70'), monitor.amount)
        self.assertEqual('+12223334444', monitor.phone_number.as_e164)
        self.assertEqual(event.id, monitor.event_id)

    def test_sets_created_status_for_monitor(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65'),
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
        )

        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('70')
        )

        monitor_status = MonitorStatus.objects.filter(monitor=monitor).latest()
        self.assertEqual(MONITOR_STATUS_CREATED, monitor_status.status)


class SetStatusOfMonitor(TestCase):

    def test_creates_new_monitor_status(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65'),
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
        )
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('70')
        )

        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)

        self.assertEqual(2, MonitorStatus.objects.filter(monitor=monitor).count())
        monitor_status = MonitorStatus.objects.filter(monitor=monitor).latest()
        self.assertEqual(MONITOR_STATUS_ACTIVATED, monitor_status.status)

    def test_raises_error_if_status_is_invalid(self):
        event = event_service.create_event(
            vendor_id='3621831',
            vendor_type=VENDOR_TYPE_SEATGEEK,
            title='Purity Ring',
            datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
            price=Decimal('65'),
            url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
        )
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('70')
        )

        with self.assertRaises(ValueError):
            monitor_service.set_status_of_monitor(monitor, 'invalid_status')
