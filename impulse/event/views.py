from django.http import HttpResponse
from django.template import Context, loader
from django.views import View

from impulse.alert.models import Monitor
from impulse.event.models import Event
from impulse.event.services import event_service


class EventDetailView(View):

    def get(self, request, event_external_id, monitor_external_id=None):
        template = loader.get_template('event/event_detail.html')
        event = Event.objects.get(external_id=event_external_id)
        if monitor_external_id:
            monitor = Monitor.objects.get(external_id=monitor_external_id)
        else:
            monitor = None

        context = Context({'event': event, 'monitor': monitor})

        return HttpResponse(template.render(context))


class EventSearchView(View):

    def get(self, request):
        query = request.GET.get('q')
        if query:
            events = event_service.find_or_create_upcoming_events_matching_query(query)
        else:
            events = None

        template = loader.get_template('event/event_search.html')
        context = Context({'query': query, 'events': events})

        return HttpResponse(template.render(context))
