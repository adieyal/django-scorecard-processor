from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.list_detail import object_list, object_detail
from django.views.generic.create_update import create_object, update_object
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

from models import Entity, Project, Survey, Question, Scorecard, ReportRun
entity_qs = Entity.objects.all().select_related('entity_type')
project_qs = Project.objects.all()
survey_qs = Survey.objects.all()
question_qs = Question.objects.all()
scorecard_qs = Scorecard.objects.all()
reportrun_qs = ReportRun.objects.all()
user_qs = User.objects.exclude(pk=settings.ANONYMOUS_USER_ID)

from views import SurveyResponses
from views import SurveyOverrides, ResponseOverrideView, ResponseOverrideDelete, create_override
from views import UserView
from views import entity_add_user, entity_remove_user
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


#Manage surveys
    url(r'^project/(\d+)/survey/(?P<object_id>\d+)/$', 
        login_required(object_detail),
        {'queryset': survey_qs}, 
        name="show_survey"
    ),

#Survey overrides
    url(r'^project/(\d+)/survey/(?P<survey_id>\d+)/override/add/$', 
        login_required(SurveyOverrides.as_view()),
        {'queryset': survey_qs}, 
        name="add_response_override"
    ),

    url(r'^project/(\d+)/survey/(\d+)/override/add/(?P<question_id>\d+)/$', 
        create_override,
        {}, 
        name="add_response_override_question"
    ),

    url(r'^project/(\d+)/survey/(\d+)/override/(?P<override_id>\d+)/$', 
        login_required(object_detail),
        {'queryset': survey_qs}, 
        name="view_response_override"
    ),

    url(r'^project/(\d+)/survey/(\d+)/override/(?P<override_id>\d+)/remove/$', 
        login_required(object_detail),
        {'queryset': survey_qs}, 
        name="remove_response_override"
    ),

#Survey responses
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


# Manage scorecards
    url(r'^project/(\d+)/scorecard/(?P<object_id>\d+)/$',
        login_required(object_detail),
        {'queryset': scorecard_qs}, 
        name="show_scorecard"
    ),

# Users
    url(r'^users/$',
        staff_member_required(object_list),
        {'queryset': user_qs}, 
        name="user_list"
    ),
    url(r'^users/(?P<pk>\d+)/$',
        staff_member_required(UserView.as_view()),
        name="show_user"
    ),

#Reports
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
    url(r'^project/(\d+)/reports/by_indicator/(?P<object_id>\d+)/(?P<indicator>\w+)/run/$',
        "indicator_report",
        name="indicator_report"
    ),


#Response side
    url(r'^entity/$', #TODO:limit entities to the ones a user account can access
        'entity_list',
        name="entity_list"
    ), 
    url(r'^entity/(?P<object_id>\d+)/$', 
        'entity_detail',
        name="show_entity"
    ),
    #Entity user management
    url(r'^entity/(?P<entity_id>\d+)/users/add/$', 
        entity_add_user,
        name="entity_add_user"
    ),
    url(r'^entity/(?P<entity_id>\d+)/users/(?P<user_id>\d+)/remove/$', 
        entity_remove_user,
        name="entity_remove_user"
    ),

    url(r'^entity/(?P<entity_id>\d+)/reports/', 
        include(get_entity_urls())
    ),
    url(r'^entity/(?P<object_id>\d+)/survey/add/(?P<survey_id>\d+)/$','add_survey',name="survey_response"),
    #TODO: urls for responses per survey
    url(r'^entity/(?P<object_id>\d+)/response/(?P<responseset_id>\d+)/edit/$','edit_survey',name="survey_response_edit"),

)

