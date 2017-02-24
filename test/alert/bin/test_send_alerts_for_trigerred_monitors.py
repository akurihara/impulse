from datetime import datetime
from decimal import Decimal
from mock import ANY, patch
import pytz

from django.test import TestCase
from freezegun import freeze_time
from twilio.rest.resources import Messages

from alert.constants import MONITOR_STATUS_ACTIVATED, OUTGOING_MESSAGE_MONITOR_TRIGGERED
from alert.bin.send_alerts_for_triggered_monitors import main
from event.lib.seatgeek_gateway import SeatGeekEvent
from test import factories


class MainTest(TestCase):

    @freeze_time('2017-01-19 3:00')
    def test_sends_sms_message_if_monitor_amount_is_less_than_event_price(self):
        event = factories.create_event()
        monitor = factories.create_monitor_for_event(
            event=event,
            amount=Decimal('65.01'),
            status=MONITOR_STATUS_ACTIVATED
        )
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            with patch.object(Messages, 'create') as twilio_mock:
                main()

        expected_body = OUTGOING_MESSAGE_MONITOR_TRIGGERED.format(
            event_title=event.title,
            amount=event.current_price.price,
            url=event.url
        )
        twilio_mock.assert_called_once_with(
            body=expected_body,
            to=monitor.phone_number.as_e164,
            from_=ANY
        )

    @freeze_time('2017-01-19 3:00')
    def test_does_not_send_sms_message_if_monitor_amount_is_higher_than_event_price(self):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            amount=Decimal('64.99'),
            status=MONITOR_STATUS_ACTIVATED
        )
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            with patch.object(Messages, 'create') as twilio_mock:
                main()

        twilio_mock.assert_not_called()

    @freeze_time('2017-01-19 2:59')
    def test_does_not_send_sms_message_if_monitor_event_starts_in_more_than_twenty_four_hours(self):
        event = factories.create_event()
        factories.create_monitor_for_event(
            event=event,
            amount=Decimal('65.01'),
            status=MONITOR_STATUS_ACTIVATED
        )
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            with patch.object(Messages, 'create') as twilio_mock:
                main()

        twilio_mock.assert_not_called()

    @freeze_time('2017-01-19 3:00')
    def test_does_not_send_sms_message_if_monitor_status_is_not_activated(self):
        event = factories.create_event()
        factories.create_monitor_for_event(event)
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            with patch.object(Messages, 'create') as twilio_mock:
                main()

        twilio_mock.assert_not_called()


def _create_mock_seatgeek_event():
    return SeatGeekEvent(
        id='3621831',
        title='Purity Ring',
        datetime_utc=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
        lowest_price=Decimal('65'),
        url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
    )
