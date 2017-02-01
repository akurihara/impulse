from datetime import datetime, time, timedelta

from alert.models import Monitor


def create_monitor_for_event(event, phone_number, amount):
    return Monitor.objects.create(
        amount=amount,
        phone_number=phone_number,
        event=event
    )
