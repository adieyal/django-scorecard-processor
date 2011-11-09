from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from models import ResponseSet, Survey, Entity
from forms import QuestionForm

def index(request):
    return render_to_response('scorecard_processor/index.html',{},RequestContext(request))

def show_survey(request, object_id, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    entity = get_object_or_404(Entity, pk=object_id)
    form = QuestionForm
    #TODO: add data series to responses
    response, created = ResponseSet.objects.get_or_create(
        survey = survey,
        respondant = request.user,
        entity = entity
    )
    if request.POST:
        form = form(request.POST, survey=survey, instance=response)
        if form.is_valid():
            form.save()
    else:
        form = form(survey=survey, instance=None)

    return render_to_response('scorecard_processor/respond/survey.html',{'entity':entity,'survey':survey, 'form':form},RequestContext(request))

