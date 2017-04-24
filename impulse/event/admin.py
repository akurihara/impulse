from django.contrib import admin

from impulse.event.models import Event, EventPrice

admin.site.register(Event)
admin.site.register(EventPrice)
