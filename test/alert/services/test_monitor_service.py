from datetime import datetime
from decimal import Decimal
import pytz

from django.test import TestCase

from alert.models import Monitor
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
