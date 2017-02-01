from datetime import datetime, timedelta
from decimal import Decimal
from mock import patch
import pytz

from django.test import TestCase

from alert.models import Monitor
from alert.services import monitor_service
from event.lib.seatgeek_gateway import Event


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

        with patch('event.lib.seatgeek_gateway.get_event_by_id', return_value=mock_event):
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
