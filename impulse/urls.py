from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import RedirectView

from alert.views import CreateMonitorView, IncomingSMSMessageView, MonitorDetailView, MonitorsHandler
from event.views import EventDetailView, EventSearchView


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='events')),
    url(r'^admin/', admin.site.urls),
    url(r'^events/$', EventSearchView.as_view(), name='events'),
    url(r'^events/(?P<event_id>[0-9]+)/$', EventDetailView.as_view(), name='event-detail'),
    url(r'^incoming-sms-message/$', IncomingSMSMessageView.as_view(), name='incoming-sms-message'),
    url(r'^monitor/add/$', CreateMonitorView.as_view(), name='monitor-create'),
    url(r'^monitor/(?P<pk>[0-9]+)/$', MonitorDetailView.as_view(), name='monitor-detail'),
    url(r'^monitors/', MonitorsHandler.as_view(), name='monitors'),
]

urlpatterns += staticfiles_urlpatterns()
