from django.conf.urls.defaults import *

from ihp_results.views import add_dsg_survey, edit_dsg_survey, view_dsg_survey

urlpatterns = patterns('',
    url(r'^(?P<entity_id>\d+)/survey_by/(?P<data_series_group_name>\w+)/add/(?P<survey_id>\d+)/$',add_dsg_survey, name="survey_dsg_response"),
    url(r'^(?P<entity_id>\d+)/response_by/(?P<data_series_group_name>\w+)/edit/(?P<survey_id>\d+)/(?P<data_series_name>[\w ]+)/$',edit_dsg_survey,name="survey_dsg_response_edit"),
    url(r'^(?P<entity_id>\d+)/response_by/(?P<data_series_group_name>\w+)/view/(?P<survey_id>\d+)/(?P<data_series_name>[\w ]+)/$',view_dsg_survey,name="survey_dsg_response_view"),
)
