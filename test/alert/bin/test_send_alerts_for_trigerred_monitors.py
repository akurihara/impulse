from datetime import datetime
from decimal import Decimal
from mock import ANY, patch
import pytz

from decimal import Decimal
from django.test import TestCase
from freezegun import freeze_time
from twilio.rest.resources import Messages

from alert.bin.send_alerts_for_triggered_monitors import main, SMS_MESSAGE_BODY
from alert.services import monitor_service
from event.lib.seatgeek_gateway import Event
from event.models import VENDOR_TYPE_SEATGEEK
from event.services import event_service



class MainTest(TestCase):

    @patch.object(Messages, 'create')
    @freeze_time('2017-01-19 3:00')
    def test_sends_sms_message_if_monitor_amount_is_less_than_event_price(self, create_mock):
        event = _create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('65.01')
        )
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            main()

        expected_body = SMS_MESSAGE_BODY.format(
            event_title=event.title,
            amount=event.current_event_price.price,
            url='www.google.com'
        )
        create_mock.assert_called_once_with(
            body=expected_body,
            to='+12223334444',
            from_=ANY
        )

    @patch.object(Messages, 'create')
    @freeze_time('2017-01-19 3:00')
    def test_does_not_send_sms_message_if_monitor_amount_is_higher_than_event_price(self, create_mock):
        event = _create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('64.99')
        )
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            main()

        create_mock.assert_not_called()

    @patch.object(Messages, 'create')
    @freeze_time('2017-01-19 2:59')
    def test_does_not_send_sms_message_if_monitor_event_starts_in_more_than_twenty_four_hours(self, create_mock):
        event = _create_event()
        monitor = monitor_service.create_monitor_for_event(
            event=event,
            phone_number='+12223334444',
            amount=Decimal('65.01')
        )
        mock_seatgeek_event = _create_mock_seatgeek_event()

        with patch('alert.bin.send_alerts_for_triggered_monitors.get_event_by_id', return_value=mock_seatgeek_event):
            main()

        create_mock.assert_not_called()


def _create_event():
    return event_service.create_event(
        vendor_id='3621831',
        vendor_type=VENDOR_TYPE_SEATGEEK,
        title='Purity Ring',
        datetime_start=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
        price=Decimal('65')
    )


def _create_mock_seatgeek_event():
    return Event(
        id='3621831',
        title='Purity Ring',
        datetime_utc=datetime(2017, 1, 20, 3, 0, tzinfo=pytz.utc),
        lowest_price=Decimal('65'),
        url='https://seatgeek.com/purity-ring-21-tickets/brooklyn-new-york-output-2017-01-19-10-pm/concert/3621831'
    )
