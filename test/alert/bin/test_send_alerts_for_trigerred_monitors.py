from decimal import Decimal
from mock import patch
from django.test import TestCase
from freezegun import freeze_time

from impulse.alert.constants import (
    MONITOR_STATUS_CREATED,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED,
    OUTGOING_MESSAGE_MONITOR_TRIGGERED
)
from impulse.alert.bin.send_alerts_for_triggered_monitors import main
from test import factories


@patch('impulse.alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=factories.create_seatgeek_event())
class MainTest(TestCase):

    @freeze_time('2017-01-19 3:00')
    @patch('impulse.alert.bin.send_alerts_for_triggered_monitors.send_sms_message')
    def test_sends_sms_message_if_monitor_amount_is_less_than_event_price(self, send_sms_message_mock, _):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(
            event=event,
            amount=Decimal('65.01'),
            status=MONITOR_STATUS_ACTIVATED
        )

        main()

        expected_body = OUTGOING_MESSAGE_MONITOR_TRIGGERED.format(
            event_title=event.title,
            amount=event.current_price.price,
            url=event.url
        )
        send_sms_message_mock.assert_called_once_with(
            to_phone_number=monitor.phone_number.as_e164,
            message=expected_body
        )

    @freeze_time('2017-01-19 3:00')
    @patch('impulse.alert.bin.send_alerts_for_triggered_monitors.send_sms_message')
    def test_does_not_send_sms_message_if_monitor_amount_is_higher_than_event_price(self, send_sms_message_mock, _):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            amount=Decimal('64.99'),
            status=MONITOR_STATUS_ACTIVATED
        )

        main()

        send_sms_message_mock.assert_not_called()

    @freeze_time('2017-01-19 2:59')
    @patch('impulse.alert.bin.send_alerts_for_triggered_monitors.send_sms_message')
    def test_does_not_send_sms_message_if_monitor_event_starts_in_more_than_twenty_four_hours(self, send_sms_message_mock, _):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            amount=Decimal('65.01'),
            status=MONITOR_STATUS_ACTIVATED
        )

        main()

        send_sms_message_mock.assert_not_called()

    @freeze_time('2017-01-19 3:00')
    @patch('impulse.alert.bin.send_alerts_for_triggered_monitors.send_sms_message')
    def test_does_not_send_sms_message_if_monitor_status_is_not_activated(self, send_sms_message_mock, _):
        event = factories.create_event()
        factories.create_monitor_for_event(event)

        main()

        send_sms_message_mock.assert_not_called()

    @freeze_time('2017-01-19 3:00')
    def test_deactivates_triggered_monitor(self, _):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(
            event=event,
            amount=Decimal('65.01'),
            status=MONITOR_STATUS_ACTIVATED
        )

        main()

        self.assertEqual(MONITOR_STATUS_DEACTIVATED, monitor.current_status.status)

    @freeze_time('2017-01-20 2:01')
    def test_deactivates_activated_monitor_of_event_starting_in_next_hour(self, _):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(
            event=event,
            amount=Decimal('64.99'),
            status=MONITOR_STATUS_ACTIVATED
        )

        main()

        self.assertEqual(MONITOR_STATUS_DEACTIVATED, monitor.current_status.status)

    @freeze_time('2017-01-20 2:01')
    def test_deactivates_created_monitor_of_event_starting_in_next_hour(self, _):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(
            event=event,
            amount=Decimal('64.99'),
            status=MONITOR_STATUS_CREATED
        )

        main()

        self.assertEqual(MONITOR_STATUS_DEACTIVATED, monitor.current_status.status)
