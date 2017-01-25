from django.contrib import admin

from event.models import Event, EventPrice

admin.site.register(Event)
admin.site.register(EventPrice)
