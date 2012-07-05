from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.views.generic.simple import direct_to_template

from ierg_results.views import graph, aggregate, summary, box, achieved, scorecard_country

admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', direct_to_template, {'template':'index.html'}),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^scorecard/', include('scorecard_processor.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),

    (r'^indicators/(?P<indicator>[.\d]+)/graph/json/$', graph),
    (r'^indicators/(?P<indicator>[.\d]+)/aggregate/json/$', aggregate),
    (r'^indicators/(?P<indicator>[.\d]+)/summary/json/$', summary),
    (r'^indicators/(?P<indicator>[.\d]+)/box/json/$', box),
    (r'^indicators/(?P<indicator>[.\d]+)/achieved/json/$', achieved),
    (r'^scorecard/country/(?P<country_id>\d+)/json/$', scorecard_country),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'static'}),
)

