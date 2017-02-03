from decimal import Decimal

from django.test import TestCase

from alert.models import MonitorStatus
from alert.services import monitor_service
from test import factories


class CurrentStatusTest(TestCase):

    def test_returns_latest_monitor_status(self):
        event = factories.create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('70')
        )

        current_status = monitor.current_status

        self.assertEqual(MonitorStatus.objects.filter(monitor=monitor).latest(), current_status)
