from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.views.generic import RedirectView

from alert.views import CreateMonitorView, MonitorDetailView, MonitorsHandler


urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='monitor-create')),
    url(r'^admin/', admin.site.urls),
    url(r'^monitor/add/$', CreateMonitorView.as_view(), name='monitor-create'),
    url(r'^monitor/(?P<pk>[0-9]+)/$', MonitorDetailView.as_view(), name='monitor-detail'),
    url(r'^monitors/', MonitorsHandler.as_view(), name='monitors'),
]

urlpatterns += staticfiles_urlpatterns()
