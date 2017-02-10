from django.test import Client, TestCase
from django.urls import reverse

from alert.constants import (
    INCOMING_MESSAGE_ACTIVATE_MONITOR,
    INCOMING_MESSAGE_DEACTIVATE_MONITOR,
    MONITOR_STATUS_ACTIVATED,
    MONITOR_STATUS_DEACTIVATED
)
from test import factories


class IncomingSMSMessageViewTest(TestCase):

    ENDPOINT = reverse('incoming-sms-message')

    def test_activates_monitor_if_activate_message_in_body(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)
        form_data = {
            'From': phone_number,
            'Body': INCOMING_MESSAGE_ACTIVATE_MONITOR
        }

        response = Client().post(self.ENDPOINT, form_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(MONITOR_STATUS_ACTIVATED, monitor.current_status.status)

    def test_deactivates_monitor_if_deactivate_message_in_body(self):
        event = factories.create_event()
        phone_number = factories.VALID_PHONE_NUMBER
        monitor = factories.create_monitor_for_event(event=event, phone_number=phone_number)
        form_data = {
            'From': phone_number,
            'Body': INCOMING_MESSAGE_DEACTIVATE_MONITOR
        }

        response = Client().post(self.ENDPOINT, form_data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(MONITOR_STATUS_DEACTIVATED, monitor.current_status.status)
