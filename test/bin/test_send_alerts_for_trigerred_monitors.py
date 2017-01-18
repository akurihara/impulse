from decimal import Decimal
from django.test import TestCase

from alert.services import monitor_service
from bin.send_alerts_for_triggered_monitors import main


class MainTest(TestCase):

    def test_sends_sms_message(self):
        monitor = monitor_service.create_monitor(
            seatgeek_event_id='3587027',
            email='alex.kurihara@gmail.com',
            amount=Decimal('70')
        )

        main()
