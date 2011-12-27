from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login, logout

from events.views import index, event_details, event_stats, add_event, profile, register
from socialstats.events.models import Event, EventStat

from django.contrib import admin
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
    (r'^event/add/$', add_event),
    (r'^event/stats/(\d+)/(\d+)/$', event_stats),
    (r'^accounts/', include('registration.backends.emailonly.urls')),
    #(r'^accounts/login/$',  login),
    #(r'^accounts/logout/$', logout),
    (r'^accounts/profile/$', profile),
    #(r'^accounts/register/$', register),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
