from datetime import datetime
from decimal import Decimal
from mock import ANY, patch
import pytz

from django.test import TestCase
from twilio.rest.resources import Messages

from alert.constants import (
    MONITOR_CONFIRMATION_MESSAGE,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_CREATED
)
from alert.models import Monitor, MonitorStatus
from alert.services import monitor_service
from event.models import VENDOR_TYPE_SEATGEEK
from event.services import event_service
from test import factories


class CreateMonitorForEventTest(TestCase):

    def test_creates_new_monitor(self):
        event = factories.create_event()

        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            amount=Decimal('70')
        )

        self.assertTrue(Monitor.objects.filter(id=monitor.id).exists())
        self.assertEqual(Decimal('70'), monitor.amount)
        self.assertEqual(factories.VALID_PHONE_NUMBER, monitor.phone_number.as_e164)
        self.assertEqual(event.id, monitor.event_id)

    def test_sets_created_status_for_monitor(self):
        event = factories.create_event()

        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            amount=Decimal('70')
        )

        self.assertEqual(1, monitor.statuses.count())
        self.assertEqual(MONITOR_STATUS_CREATED, monitor.current_status.status)

    @patch.object(Messages, 'create')
    def test_sends_monitor_confirmation_message(self, twilio_mock):
        event = factories.create_event()

        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            amount=Decimal('70')
        )

        expected_body = MONITOR_CONFIRMATION_MESSAGE.format(event_title=event.title)
        twilio_mock.assert_called_once_with(
            body=expected_body,
            to=factories.VALID_PHONE_NUMBER,
            from_=ANY
        )


class SetStatusOfMonitor(TestCase):

    def test_creates_new_monitor_status(self):
        event = factories.create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            amount=Decimal('70')
        )

        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)

        self.assertEqual(2, monitor.statuses.count())
        self.assertEqual(MONITOR_STATUS_ACTIVATED, monitor.current_status.status)

    def test_raises_error_if_status_is_invalid(self):
        event = factories.create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            amount=Decimal('70')
        )

        with self.assertRaises(ValueError):
            monitor_service.set_status_of_monitor(monitor, 'invalid_status')
