from django.conf.urls.defaults import *

urlpatterns = patterns('ihp_results.views',
    url(r'^import/(?P<agency_id>\d+)$', 'import_response', name="import_response"),

    url(r'^reports/entity/(?P<agency_id>\d+)/$', 'entity_report', name="ihp_entity_report"),
    url(r'^reports/entity/(?P<agency_id>\d+)/(?P<output_format>\w+)/$', 'entity_report', name="ihp_entity_report_output"),

    url(r'^reports/entity_indicator/(?P<scorecard_id>\d+)/(?P<identifier>\w+)/$', 'indicator_by_entity', name="scorecard_entity_indicator_report"),
    url(r'^reports/entity_indicator/(?P<scorecard_id>\d+)/(?P<identifier>\w+)/(?P<output_format>\w+)/$', 'indicator_by_entity', name="scorecard_entity_indicator_report_output"),

    url(r'^reports/grouped_indicator/(?P<scorecard_id>\d+)/(?P<data_series_group_name>\w+)/(?P<identifier>\w+)/$', 'indicator_by_group', name="scorecard_group_indicator_report"),
    url(r'^reports/grouped_indicator/(?P<scorecard_id>\d+)/(?P<data_series_group_name>\w+)/(?P<identifier>\w+)/(?P<output_format>\w+)/$', 'indicator_by_group', name="scorecard_group_indicator_report_output"),

)

