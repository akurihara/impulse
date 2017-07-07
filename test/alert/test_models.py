from django.test import TestCase

from impulse.alert.constants import (
    MONITOR_STATUS_CREATED,
    MONITOR_STATUS_DEACTIVATED
)
from impulse.alert.models import Monitor, MonitorStatus
from test import factories


class CurrentStatusTest(TestCase):

    def test_returns_latest_monitor_status(self):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(event)

        current_status = monitor.current_status

        self.assertEqual(MonitorStatus.objects.filter(monitor=monitor).latest(), current_status)


class FilterStatusesTest(TestCase):

    def test_returns_monitors_with_statuses(self):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            status=MONITOR_STATUS_DEACTIVATED
        )
        created_monitor = factories.create_monitor_for_event(
            event=event,
            status=MONITOR_STATUS_CREATED
        )

        created_monitors = Monitor.filter_statuses([MONITOR_STATUS_CREATED])

        self.assertEqual(1, len(created_monitors))
        self.assertEqual(created_monitor.id, created_monitors[0].id)
