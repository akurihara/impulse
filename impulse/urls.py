from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import RedirectView

from alert.views import CreateMonitorView, IncomingSMSMessageView
from event.views import EventDetailView, EventSearchView


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='events')),
    url(r'^admin/', admin.site.urls),
    url(r'^events$', EventSearchView.as_view(), name='events'),
    url(r'^events/(?P<event_external_id>[a-z]+)$', EventDetailView.as_view(), name='event-detail'),
    url(
        r'^events/(?P<event_external_id>[a-z]+)/monitors$',
        CreateMonitorView.as_view(), name='create-monitor'
    ),
    url(
        r'^events/(?P<event_external_id>[a-z]+)/monitors/(?P<monitor_external_id>[a-z]+)$',
        EventDetailView.as_view(), name='event-with-monitor-detail'
    ),
    url(r'^incoming-sms-message$', IncomingSMSMessageView.as_view(), name='incoming-sms-message'),
]

urlpatterns += staticfiles_urlpatterns()
