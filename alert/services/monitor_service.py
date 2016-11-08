from alert.models import Monitor
from lib import seatgeek_gateway


def create_monitor(seatgeek_event_id, email, amount):
    event = seatgeek_gateway.get_event_by_id(seatgeek_event_id)

    return Monitor.objects.create(
        amount=amount,
        datetime_event_start=event.datetime_utc,
        event_title=event.title,
        email=email,
        seatgeek_event_id=seatgeek_event_id
    )
