from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

from models import ResponseSet, Survey, Entity
from forms import QuestionForm, ResponseSetForm

def index(request):
    return render_to_response('scorecard_processor/index.html',{},RequestContext(request))

@login_required
def add_survey(request, object_id, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    entity = get_object_or_404(Entity, pk=object_id)
    instance = ResponseSet(
                    respondant=request.user, 
                    survey=survey,
                    entity=entity
                )
    form = ResponseSetForm
    if request.POST:
        form = form(request.POST, instance = instance)
        if form.is_valid():
            responseset = form.save()
            #TODO: check that there isn't already a response for the given data series, if there is, return that instead
            return HttpResponseRedirect(responseset.get_absolute_url())
    else:
        form = form(instance = instance)
    return render_to_response('scorecard_processor/respond/add_survey.html',{'survey':survey, 'entity':entity, 'form':form},RequestContext(request))

@login_required
def edit_survey(request, object_id, responseset_id):
    #TODO handle dataset updates/additions/listing
    responseset = get_object_or_404(ResponseSet, pk=responseset_id)
    survey = responseset.survey
    entity = get_object_or_404(Entity, pk=object_id)
    form = QuestionForm
    
    if request.POST:
        form = form(request.POST, survey=survey, instance=responseset)#, user=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('%s#responseset_%s' % (responseset.entity.get_absolute_url(), responseset.pk))
    else:
        form = form(survey=survey, instance=responseset)

    return render_to_response('scorecard_processor/respond/edit_survey.html',{'responseset':responseset,'entity':entity,'survey':survey, 'form':form},RequestContext(request))

