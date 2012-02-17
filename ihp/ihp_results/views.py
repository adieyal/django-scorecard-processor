# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import DetailView, ListView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from scorecard_processor.models import Entity, DataSeriesGroup, Survey

@login_required
def add_dsg_survey(request, entity_id, data_series_group_name, survey_id):
    entity = Entity.objects.get(pk=entity_id)
    if not request.user.is_staff and request.user.entity_set.filter(pk=entity.pk).count() == 0:
        raise Http404
    data_series_group = DataSeriesGroup.objects.get(pk=data_series_group_name)
    survey = Survey.objects.get(pk=survey_id)
    if entity.entity_type_id == 'government':
        data_series = data_series_group.dataseries_set.filter(name=entity.abbreviation)
    else:
        data_series = data_series_group.dataseries_set.all()
    if len(data_series) == 1:
        return HttpResponseRedirect(reverse("survey_dsg_response_edit",args=[entity.pk, data_series_group.pk, survey.pk, data_series[0].name]))
    context = {
        'entity':entity,
        'survey':survey,
        'data_series_group':data_series_group,
        'data_series':data_series
    }
    return render_to_response('ihp_results/add_dsg_survey.html',context,RequestContext(request))

from forms import QuestionForm

@login_required
def edit_dsg_survey(request, entity_id, data_series_group_name, survey_id, data_series_name):
    entity = Entity.objects.get(pk=entity_id)
    if not request.user.is_staff and request.user.entity_set.filter(pk=entity.pk).count() == 0:
        return Http404
    data_series_group = DataSeriesGroup.objects.get(pk=data_series_group_name)
    try:
        ds_pk = int(data_series_name)
    except ValueError:
        ds_pk = None
    if ds_pk:
        data_series = data_series_group.dataseries_set.get(pk=data_series_name)
    else:
        data_series = data_series_group.dataseries_set.get(name=data_series_name)

    if entity.entity_type_id == 'government' and data_series.name != entity.abbreviation:
        raise Http404

    survey = Survey.objects.get(pk=survey_id)
    categories = DataSeriesGroup.objects.get(pk='Data collection year').dataseries_set.filter(visible=True)

    if request.POST:
        form = QuestionForm(request.POST, entity=entity, user=request.user, survey=survey, country=data_series, series=categories)
        if form.is_valid():
            form.save()
            next_section = request.POST.get('next')
            if next_section:
                return HttpResponseRedirect('#%s' % next_section)
            else:
                return HttpResponseRedirect(entity.get_absolute_url()+"#"+data_series.name)
    else:
        form = QuestionForm(entity=entity, user=request.user, survey=survey, country=data_series, series=categories)

    context = {
        'entity':entity,
        'survey':survey,
        'data_series_group':data_series_group,
        'form':form,
        'data_series':data_series
    }
    return render_to_response('ihp_results/edit_dsg_survey.html',context,RequestContext(request))
