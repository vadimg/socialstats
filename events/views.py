from django.db.models import Max
from django.db import IntegrityError
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response

from events.models import Event, EventStat
from events.forms import AddEventForm
from events.tasks import monitor_stats

import datetime
import dateutil.parser
import time
import simplejson
import re

from grabber.facebook import Api

fb_api = Api()

def index(req):
    events = Event.objects.all().select_related()
    ret = []
    for e in events:
        s = e.eventstat_set.latest('time')
        ret.append(make_event(e, s))

    return render_to_response('index.html', {
        'events': ret
    })

def register(req):
    form = UserCreationForm()
    if req.method == 'POST':
        data = req.POST.copy()
        print dir(form)
        errors = form.get_validation_errors(data)
        if not errors:
            new_user = form.save()
            return HttpResponseRedirect("/accounts/created/")
    else:
        context = { 'form': form }
        return render_to_response("registration/register.html", context, context_instance=RequestContext(req))

@login_required
def profile(req):
    events = Event.objects.filter(user=req.user.id).select_related()
    ret = []
    for e in events:
        s = e.eventstat_set.latest('time')
        ret.append(make_event(e, s))

    return render_to_response('index.html', {
        'events': ret
    })

def event_details(req, event_id):
    event_id = make_int(event_id)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        raise Http404()

    ret = make_event(event, event.eventstat_set.latest('time'))
    return render_to_response('event_details.html', { 'event': ret })

def event_stats(req, event_id, start):
    event_id = make_int(event_id)
    start = make_datetime(start)

    # TODO: this is very bad
    stats = EventStat.objects.filter(event=event_id, time__gte=start)
    arr = make_objarr(stats, ('invited', 'going', 'maybe', 'time'))
    return HttpResponse(JSONEncoder().encode(arr), mimetype='application/json')

@login_required
def add_event(req):
    if req.method == 'POST':
        form = AddEventForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            url = data.get('event_url')
            match = re.search(r'://(www\.)?facebook.com/events/(\d+)', url)
            if match:
                event_id = int(match.group(2))

                if not Event.objects.filter(id=event_id).exists():
                    # only get event data if event wasn't already added
                    # TODO: let user know event was already added
                    event = fb_api.get_info(event_id)

                    name = event[u'name']
                    start = dateutil.parser.parse(event[u'start_time'])
                    end = dateutil.parser.parse(event[u'end_time'])

                    Event.objects.create(user_id=req.user.id,
                                         id=event_id,
                                         name=name,
                                         start=start,
                                         end=end)
                    monitor_stats.delay(event_id)

                return HttpResponseRedirect('/event/{0}'.format(event_id))
    else:
        form = AddEventForm()

    context = {
        'form': form
    }
    return render_to_response('add_event.html', context, context_instance=RequestContext(req))


class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(time.mktime(obj.timetuple()))
        else:
            return simplejson.JSONEncoder.default(self, obj)

def make_int(s):
    try:
        return int(s)
    except Exception:
        raise Http404()

def make_datetime(s):
    try:
        return datetime.datetime.fromtimestamp(int(s))
    except Exception:
        raise Http404()

def make_objarr(qs, fields):
    """return an array of objects for all rows in the QuerySet"""
    ret = []
    for o in qs:
        d = []
        for attr in fields:
            d.append(getattr(o, attr))
        ret.append(d)
    return ret

def make_event(event, stat):
    return {
        'id': event.id,
        'name': event.name,
        'start': event.start,
        'end': event.end,
        'invited': stat.invited,
        'going': stat.going,
        'maybe': stat.maybe,
    }

