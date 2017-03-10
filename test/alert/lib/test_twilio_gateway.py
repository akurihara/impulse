from django.test import TestCase
from twilio.twiml import Response

from alert.lib.twilio_gateway import create_twiml_response, send_sms_message
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


class CreateTwiMLResponseTest(TestCase):

    def test_returns_twiml_response_instance(self):
        message = 'Hello there'

        twiml_response = create_twiml_response(message)

        self.assertIsInstance(twiml_response, Response)
