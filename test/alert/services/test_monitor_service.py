from datetime import datetime
from decimal import Decimal
from mock import ANY, patch
import pytz

from django.test import TestCase
from twilio.rest.resources import Messages

from alert.constants import (
    MONITOR_CONFIRMATION_MESSAGE,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_CREATED,
    MONITOR_STATUS_DEACTIVATED
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


class GetActiveMonitorByPhoneNumberTest(TestCase):

    def test_returns_monitor_with_activated_status(self):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(event)
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)

        active_monitor = monitor_service.get_active_monitor_by_phone_number(factories.VALID_PHONE_NUMBER)

        self.assertEqual(monitor, active_monitor)

    def test_returns_monitor_for_given_phone_number_when_active_monitors_exist_for_multiple_phone_numbers(self):
        event = factories.create_event()
        first_monitor = factories.create_monitor_for_event(event)
        second_monitor = factories.create_monitor_for_event(event, phone_number='+13106172186')
        monitor_service.set_status_of_monitor(first_monitor, MONITOR_STATUS_ACTIVATED)
        monitor_service.set_status_of_monitor(second_monitor, MONITOR_STATUS_ACTIVATED)

        active_monitor = monitor_service.get_active_monitor_by_phone_number(factories.VALID_PHONE_NUMBER)

        self.assertEqual(first_monitor, active_monitor)

    def test_returns_none_if_monitors_has_been_created_but_not_activated(self):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(event)

        active_monitor = monitor_service.get_active_monitor_by_phone_number(factories.VALID_PHONE_NUMBER)

        self.assertIsNone(active_monitor)

    def test_returns_none_if_monitor_has_been_deactivated(self):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(event)
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)

        active_monitor = monitor_service.get_active_monitor_by_phone_number(factories.VALID_PHONE_NUMBER)

        self.assertIsNone(active_monitor)
