from django.contrib import admin

from impulse.alert.models import Monitor, MonitorStatus

admin.site.register(Monitor)
admin.site.register(MonitorStatus)
