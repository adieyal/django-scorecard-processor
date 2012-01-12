from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.contrib.auth.decorators import login_required

from models import Entity, Project, Survey, Question, Scorecard, ReportRun
entity_qs = Entity.objects.all().select_related('entity_type')
project_qs = Project.objects.all()
survey_qs = Survey.objects.all()
question_qs = Question.objects.all()
scorecard_qs = Scorecard.objects.all()
reportrun_qs = ReportRun.objects.all()

from views import SurveyResponses
from reports import get_entity_urls, get_project_urls

urlpatterns = patterns('scorecard_processor.views',
    url(r'^$', 'index', name="scorecard_index"),

#Projects, surveys and scorecards
#TODO:limit entities to the ones a user account can access
    url(r'^project/$', 
        login_required(object_list), 
        {'queryset':project_qs},
        name="project_list"
    ), 
    url(r'^project/(?P<object_id>\d+)/$', 
        login_required(object_detail),
        {'queryset':project_qs}, 
        name="show_project"
    ),

    url(r'^project/(\d+)/survey/(?P<object_id>\d+)/$', 
        login_required(object_detail),
        {'queryset': survey_qs}, 
        name="show_survey"
    ),

    url(r'^project/(\d+)/survey/(?P<object_id>\d+)/responses/$', 
        login_required(SurveyResponses.as_view()),
        name="show_survey_responses"
    ),

    url(r'^project/(\d+)/survey/(?P<object_id>\d+)/responses/series/(?P<series>[\w\ ]+)/$', 
        login_required(SurveyResponses.as_view()),
        name="show_survey_responses_series"
    ),

    url(r'^project/(\d+)/survey/(?P<object_id>\d+)/responses/entity/(?P<entity>\d+)/$', 
        login_required(SurveyResponses.as_view()),
        name="show_survey_responses_entity"
    ),

    url(r'^project/(\d+)/scorecard/(?P<object_id>\d+)/$',
        login_required(object_detail),
        {'queryset': scorecard_qs}, 
        name="show_scorecard"
    ),

    url(r'^project/(\d+)/reports/generic/(?P<object_id>\d+)/$',
        login_required(object_detail),
        {'queryset': reportrun_qs}, 
        name="show_report"
    ),
    url(r'^project/(\d+)/reports/generic/(?P<object_id>\d+)/run/$',
        "run_report",
        name="run_report"
    ),
    url(r'^project/(?P<project_id>\d+)/reports/', 
        include(get_project_urls())
    ),


#Response side
    url(r'^entity/$', #TODO:limit entities to the ones a user account can access
        login_required(object_list), 
        {'queryset':entity_qs},
        name="entity_list"
    ), 
    url(r'^entity/(?P<object_id>\d+)/$', 
        login_required(object_detail),
        {'queryset':entity_qs}, 
        name="show_entity"
    ),
    url(r'^entity/(?P<entity_id>\d+)/reports/', 
        include(get_entity_urls())
    ),
    url(r'^entity/(?P<object_id>\d+)/survey/add/(?P<survey_id>\d+)/$','add_survey',name="survey_response"),
    #TODO: urls for responses per survey
    url(r'^entity/(?P<object_id>\d+)/response/(?P<responseset_id>\d+)/edit/$','edit_survey',name="survey_response_edit"),
)

