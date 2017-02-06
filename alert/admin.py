from django.contrib import admin

from alert.models import Monitor, MonitorStatus

admin.site.register(Monitor)
admin.site.register(MonitorStatus)
