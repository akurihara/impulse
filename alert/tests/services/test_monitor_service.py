from decimal import Decimal

from django.test import TestCase

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
