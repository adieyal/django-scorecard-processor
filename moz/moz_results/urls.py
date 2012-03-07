from django.conf.urls.defaults import *

urlpatterns = patterns('moz_results.views',
    url(r'^import/(?P<agency_id>\d+)$', 'import_response', name="import_response"),
)

