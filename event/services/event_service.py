from event.models import Event, EventPrice


def create_event(vendor_id, vendor_type, title, datetime_start, price):
    event = Event.objects.create(
        datetime_start=datetime_start,
        title=title,
        vendor_id=vendor_id,
        vendor_type=vendor_type,
    )
    create_event_price_for_event(event, price)

    return event


def create_event_price_for_event(event, price):
    EventPrice.objects.create(
        event=event,
        price=price
    )
