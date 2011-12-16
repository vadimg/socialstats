from grabber.facebook import Facebook

from events.models import EventStat

from celery.task import task

fb = Facebook()

@task
def monitor_stats(event_id):
    print 'running grab'
    # push to queue before doing anything in case there's an error
    monitor_stats.delay(event_id)

    stats = fb.get_stats(event_id)
    EventStat.objects.create(event_id=event_id, **stats)

