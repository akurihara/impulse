from django.test import TestCase

from impulse.alert.models import MonitorStatus
from test import factories


class CurrentStatusTest(TestCase):

    def test_returns_latest_monitor_status(self):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(event)

        current_status = monitor.current_status

        self.assertEqual(MonitorStatus.objects.filter(monitor=monitor).latest(), current_status)
