from django.test import TestCase

from alert.lib.twilio_gateway import send_sms_message
from test.factories import VALID_PHONE_NUMBER


class SendSMSMessageTest(TestCase):

    def test_sends_successful_message(self):
        message = 'Hello there'
        phone_number = VALID_PHONE_NUMBER

        twilio_message = send_sms_message(
            to_phone_number=phone_number,
            message=message
        )

        expected_message = 'Sent from your Twilio trial account - {}'.format(message)
        self.assertEqual(expected_message, twilio_message.body)
        self.assertEqual(phone_number, twilio_message.to)
        self.assertEqual('queued', twilio_message.status)
