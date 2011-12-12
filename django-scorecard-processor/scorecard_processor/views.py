from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required

from models import ResponseSet, Survey, Entity, ReportRun, DataSeries
from forms import QuestionForm, ResponseSetForm

def index(request):
    return render_to_response('scorecard_processor/index.html',{},RequestContext(request))

#################################################################
# Managing reporting, surveys etc.
#################################################################

class SurveyResponses(ListView):
    paginate_by = 20
    def get_queryset(self):
        self.survey = get_object_or_404(Survey, pk=self.kwargs['object_id'])
        qs = ResponseSet.objects.filter(survey=self.survey).select_related('entity').order_by('entity__name')
        self.series = self.kwargs.get('series')
        if self.series:
            qs = qs.filter(data_series__name=self.series)
        self.entity = self.kwargs.get('entity')
        if self.entity:
            self.entity = get_object_or_404(Entity, pk=self.entity)
            qs = qs.filter(entity=self.entity)
        self.count = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super(SurveyResponses,self).get_context_data(**kwargs)
        context['survey'] = self.survey
        context['count'] = self.count
        context['series'] = self.series
        context['entity'] = self.entity
        return context

def run_report(request, object_id):
    obj = get_object_or_404(ReportRun, pk=object_id)
    return render_to_response(
        'scorecard_processor/reportrun_run.html',
        {'object':obj, 'report':obj.run()},
        RequestContext(request)
    )


#################################################################
# User response section
#################################################################

@login_required
def add_survey(request, object_id, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    entity = get_object_or_404(Entity, pk=object_id)
    instance = ResponseSet(
                    survey=survey,
                    entity=entity
                )
    form = ResponseSetForm
    if request.POST:
        form = form(request.POST, instance = instance)
        if form.is_valid():
            responseset = form.save()
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
        form = form(request.POST, survey=survey, instance=responseset, user=request.user)
        if form.is_valid():
            form.save()
            next_section = request.POST.get('next')
            if next_section:
                return HttpResponseRedirect('%s#%s' % (responseset.get_absolute_url(), next_section))
            else:
                return HttpResponseRedirect('%s#responseset_%s' % (responseset.entity.get_absolute_url(), responseset.pk))
    else:
        form = form(survey=survey, instance=responseset, user=request.user)

    return render_to_response('scorecard_processor/respond/edit_survey.html',{'responseset':responseset,'entity':entity,'survey':survey, 'form':form},RequestContext(request))

