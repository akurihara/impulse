from django.shortcuts import render
from django.template import Context
from django.views import View

from impulse.alert.models import Monitor
from impulse.event.models import Event
from impulse.event.services import event_service


class EventDetailView(View):

    def get(self, request, event_external_id, monitor_external_id=None):
        event = Event.objects.get(external_id=event_external_id)
        if monitor_external_id:
            monitor = Monitor.objects.get(external_id=monitor_external_id)
        else:
            monitor = None

        context = Context({'event': event, 'monitor': monitor})

        return render(request, 'event/event_detail.html', context)


class EventSearchView(View):

    def get(self, request):
        query = request.GET.get('q')
        if query:
            events = event_service.find_or_create_upcoming_events_matching_query(query)
        else:
            events = None

        context = Context({'query': query, 'events': events})

        return render(request, 'event/event_search.html', context)
