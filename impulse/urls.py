from django.conf import settings
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin

from alert.views import MonitorsHandler


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^monitors/', MonitorsHandler.as_view(), name='monitors'),
]

urlpatterns += staticfiles_urlpatterns()
