from datetime import datetime
from decimal import Decimal
from mock import ANY, patch
import pytz

from django.test import TestCase
from twilio.rest.resources import Messages

from alert.constants import (
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_CREATED,
    MONITOR_STATUS_DEACTIVATED,
    OUTGOING_MESSAGE_MONITOR_CONFIRMATION
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

        expected_body = OUTGOING_MESSAGE_MONITOR_CONFIRMATION.format(event_title=event.title)
        twilio_mock.assert_called_once_with(
            body=expected_body,
            to=factories.VALID_PHONE_NUMBER,
            from_=ANY
        )

    def test_raises_error_if_created_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            status=MONITOR_STATUS_CREATED
        )

        with self.assertRaises(ValueError):
            monitor_service.create_monitor_for_event(
                event=event,
                phone_number=factories.VALID_PHONE_NUMBER,
                amount=Decimal('80')
            )

    def test_raises_error_if_activated_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            status=MONITOR_STATUS_ACTIVATED
        )

        with self.assertRaises(ValueError):
            monitor_service.create_monitor_for_event(
                event=event,
                phone_number=factories.VALID_PHONE_NUMBER,
                amount=Decimal('70')
            )

    def test_does_not_raise_error_if_deactivated_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number=factories.VALID_PHONE_NUMBER,
            amount=Decimal('70')
        )
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)

        try:
            monitor_service.create_monitor_for_event(
                event=event,
                phone_number=factories.VALID_PHONE_NUMBER,
                amount=Decimal('80')
            )
        except ValueError:
            self.fail('create_monitor_for_event should not raise if existing monitors are deactivated')


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


class DoesActivatedOrCreatedMonitorExistForPhoneNumberTest(TestCase):

    def test_returns_true_if_activated_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_ACTIVATED)

        self.assertTrue(
            monitor_service.does_activated_or_created_monitor_exist_for_phone_number(phone_number)
        )

    def test_returns_true_if_created_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)

        self.assertTrue(
            monitor_service.does_activated_or_created_monitor_exist_for_phone_number(phone_number)
        )

    def test_returns_false_if_monitor_for_phone_number_has_been_deactivated(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)
        monitor_service.set_status_of_monitor(monitor, MONITOR_STATUS_DEACTIVATED)

        self.assertFalse(
            monitor_service.does_activated_or_created_monitor_exist_for_phone_number(phone_number)
        )


class GetCreatedMonitorForPhoneNumberTest(TestCase):

    def test_returns_true_if_created_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)

        actual_monitor = monitor_service.get_created_monitor_for_phone_number(phone_number)

        self.assertEqual(monitor, actual_monitor)

    def test_returns_monitor_if_created_monitors_exists_for_multiple_phone_numbers(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        first_monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)
        second_monitor = factories.create_monitor_for_event(event=event, phone_number='+13106172186')

        actual_monitor = monitor_service.get_created_monitor_for_phone_number(phone_number)

        self.assertEqual(first_monitor, actual_monitor)

    def test_returns_none_if_monitor_exists_for_phone_number_but_does_not_have_created_status(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(
            event=event,
            phone_number=phone_number,
            status=MONITOR_STATUS_ACTIVATED
        )

        self.assertIsNone(monitor_service.get_created_monitor_for_phone_number(phone_number))

    def test_returns_none_if_no_monitors_exist_for_phone_number(self):
        phone_number = factories.VALID_PHONE_NUMBER

        self.assertIsNone(monitor_service.get_created_monitor_for_phone_number(phone_number))


class GetActivatedMonitorForPhoneNumberTest(TestCase):

    def test_returns_true_if_activated_monitor_exists_for_phone_number(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(
            event=event,
            phone_number=phone_number,
            status=MONITOR_STATUS_ACTIVATED
        )

        actual_monitor = monitor_service.get_activated_monitor_for_phone_number(phone_number)

        self.assertEqual(monitor, actual_monitor)

    def test_returns_monitor_if_activated_monitors_exists_for_multiple_phone_numbers(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        first_monitor = factories.create_monitor_for_event(
            event=event,
            phone_number=phone_number,
            status=MONITOR_STATUS_ACTIVATED
        )
        second_monitor = factories.create_monitor_for_event(
            event=event,
            phone_number='+13106172186',
            status=MONITOR_STATUS_ACTIVATED
        )

        actual_monitor = monitor_service.get_activated_monitor_for_phone_number(phone_number)

        self.assertEqual(first_monitor, actual_monitor)

    def test_returns_none_if_monitor_exists_for_phone_number_but_does_not_have_activated_status(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)

        self.assertIsNone(monitor_service.get_activated_monitor_for_phone_number(phone_number))

    def test_returns_none_if_no_monitors_exist_for_phone_number(self):
        phone_number = factories.VALID_PHONE_NUMBER

        self.assertIsNone(monitor_service.get_activated_monitor_for_phone_number(phone_number))
