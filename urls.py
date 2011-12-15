from django.conf.urls.defaults import patterns, include, url

from events.views import index, event_details, event_stats
from django.contrib import admin
from socialstats.events.models import Event, EventStat
admin.site.register(Event)
admin.site.register(EventStat)
admin.autodiscover()

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'socialstats.views.home', name='home'),
    # url(r'^socialstats/', include('socialstats.foo.urls')),
    (r'^$', index),
    (r'^admin/', include(admin.site.urls)),
    (r'^event/(\d+)/$', event_details),
    (r'^event_stats/(\d+)/(\d+)/(\d+)$', event_stats),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
