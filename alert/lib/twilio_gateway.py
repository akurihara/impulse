import os

from twilio import twiml
from twilio.rest import TwilioRestClient


def send_sms_message(to_phone_number, message):
    twilio_number, twilio_account_sid, twilio_auth_token = _load_twilio_configuration()
    twilio_client = TwilioRestClient(twilio_account_sid, twilio_auth_token)

    return twilio_client.messages.create(
        body=message,
        to=to_phone_number,
        from_=twilio_number
    )


def _load_twilio_configuration():
    twilio_account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    twilio_auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    twilio_number = os.environ.get('TWILIO_NUMBER')

    return twilio_number, twilio_account_sid, twilio_auth_token


def create_twiml_response(message):
    twiml_response = twiml.Response()
    twiml_response.message(message)

    return twiml_response
