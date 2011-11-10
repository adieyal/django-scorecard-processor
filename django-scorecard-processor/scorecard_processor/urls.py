from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_list, object_detail
from django.contrib.auth.decorators import login_required

from models import Entity

urlpatterns = patterns('scorecard_processor.views',
    url(r'^$', 'index', name="scorecard_index"),
    url(r'^entity/$', #TODO:limit entities to the ones a user account can access
        login_required(object_list), 
        {'queryset':Entity.objects.all()},
        name="entity_list"
    ), 
    url(r'^entity/(?P<object_id>\d+)/$', 
        login_required(object_detail),
        {'queryset':Entity.objects.all()}, 
        name="show_entity"
    ),
    #TODO: should be keyed off response set id, since an entity might respond multiple times
    url(r'^entity/(?P<object_id>\d+)/survey/(?P<survey_id>\d+)/add/$','edit_survey',name="survey_response"),
)

