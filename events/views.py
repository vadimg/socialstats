from django.core import serializers
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from events.models import Event, EventStat

import datetime
import time
import simplejson

def index(req):
    events = Event.objects.all()

    return render_to_response('index.html', {
        'events': events
    })

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
        d = {}
        for attr in fields:
            d[attr] = getattr(o, attr)
        ret.append(d)
    return ret

def event_details(req, event_id):
    event_id = make_int(event_id)

    event = Event.objects.get(id=event_id)
    return render_to_response('event_details.html', { 'event': event })

def event_stats(req, event_id, start, end):
    event_id = make_int(event_id)
    start = make_datetime(start)
    end = make_datetime(end)

    # TODO: this is very bad
    stats = EventStat.objects.filter(time__gte=start, time__lte=end)
    arr = make_objarr(stats, ('invited', 'attending', 'maybe', 'time'))
    return HttpResponse(JSONEncoder().encode(arr))

class JSONEncoder(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(time.mktime(obj.timetuple()))
        else:
            return simplejson.JSONEncoder.default(self, obj)
