from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from models import Entity, Project, Survey
entity_qs = Entity.objects.all()
project_qs = Project.objects.all()
survey_qs = Survey.objects.all()

urlpatterns = patterns('scorecard_processor.views',
    url(r'^$', 'index', name="scorecard_index"),

#Projects, surveys and scorecards
    url(r'^project/$', #TODO:limit entities to the ones a user account can access
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
        name="show_project"
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
    url(r'^entity/(?P<object_id>\d+)/survey/add/(?P<survey_id>\d+)/$','add_survey',name="survey_response"),
    #TODO: urls for responses per survey
    url(r'^entity/(?P<object_id>\d+)/response/(?P<responseset_id>\d+)/edit/$','edit_survey',name="survey_response_edit"),
)

