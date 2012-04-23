from django.conf.urls.defaults import *

urlpatterns = patterns('ihp_results.views',
    url(r'^import/(?P<agency_id>\d+)$', 'import_response', name="import_response"),
    url(r'^reports/entity/(?P<agency_id>\d+)/$', 'entity_report', name="ihp_entity_report"),

)

