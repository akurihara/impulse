MONITOR_STATUS_CREATED = 0
MONITOR_STATUS_ACTIVATED = 1
MONITOR_STATUS_DEACTIVATED = 2

MONITOR_STATUSES = {
    MONITOR_STATUS_CREATED: 'Created',
    MONITOR_STATUS_ACTIVATED: 'Activated',
    MONITOR_STATUS_DEACTIVATED: 'Deactivated'
}

MONITOR_CONFIRMATION_MESSAGE = '''This number was registered to track ticket prices for {event_title}. Please reply:

1: confirm
2: cancel
'''

MONITOR_TRIGGERED_MESSAGE = '''Lowest price for {event_title} is ${amount}!

Buy tickets at {url}
'''
