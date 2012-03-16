# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import DetailView, ListView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User

from guardian.shortcuts import get_perms, assign, remove_perm, get_objects_for_user


from scorecard_processor.models import Entity, DataSeriesGroup, Survey, DataSeries

@login_required
def add_dsg_survey(request, entity_id, data_series_group_name, survey_id):
    entity = Entity.objects.get(pk=entity_id)
    if not request.user.is_staff and 'change_entity' not in get_perms(request.user, entity):
        raise Http404
    data_series_group = DataSeriesGroup.objects.get(pk=data_series_group_name)
    survey = Survey.objects.get(pk=survey_id)
    if entity.entity_type_id == 'government':
        data_series = data_series_group.dataseries_set.filter(name=entity.abbreviation)
    else:
        data_series = get_objects_for_user(request.user, 'can_use', data_series_group.dataseries_set.all())
        if len(data_series) == 0:
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
    survey = Survey.objects.get(pk=survey_id)
    if not request.user.is_staff and 'change_entity' not in get_perms(request.user, entity) or survey.active == False:
        raise Http404

    data_series_group = DataSeriesGroup.objects.get(pk=data_series_group_name)
    data_series = get_objects_for_user(request.user, 'can_use', data_series_group.dataseries_set.all())
    if len(data_series) == 0:
        data_series = data_series_group.dataseries_set.all()
    key = {}
    try:
        key['pk'] = int(data_series_name)
    except ValueError:
        key['name'] = data_series_name
    data_series = get_object_or_404(data_series, **key)

    if entity.entity_type_id == 'government' and data_series.name != entity.abbreviation:
        raise Http404


    categories = DataSeriesGroup.objects.get(pk='Data collection year').dataseries_set.filter(visible=True)

    if request.POST:
        form = QuestionForm(request.POST, entity=entity, user=request.user, survey=survey, country=data_series, series=categories)
        if form.is_valid():
            form.save()
            next_section = request.POST.get('next')
            if next_section:
                return HttpResponseRedirect('#%s' % next_section)
            else:
                return HttpResponseRedirect(entity.get_absolute_url()+"#responseset_"+data_series.name)
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

@login_required
def view_dsg_survey(request, entity_id, data_series_group_name, survey_id, data_series_name):
    entity = Entity.objects.get(pk=entity_id)
    survey = Survey.objects.get(pk=survey_id)
    if not request.user.is_staff and 'change_entity' not in get_perms(request.user, entity) or survey.active == False:
        raise Http404

    data_series_group = DataSeriesGroup.objects.get(pk=data_series_group_name)
    data_series = get_objects_for_user(request.user, 'can_use', data_series_group.dataseries_set.all())
    if len(data_series) == 0:
        data_series = data_series_group.dataseries_set.all()
    key = {}
    try:
        key['pk'] = int(data_series_name)
    except ValueError:
        key['name'] = data_series_name
    data_series = get_object_or_404(data_series, **key)

    if entity.entity_type_id == 'government' and data_series.name != entity.abbreviation:
        raise Http404


    categories = DataSeriesGroup.objects.get(pk='Data collection year').dataseries_set.filter(visible=True)

    form = QuestionForm(entity=entity, user=request.user, survey=survey, country=data_series, series=categories, static=True)
    context = {
        'entity':entity,
        'survey':survey,
        'data_series_group':data_series_group,
        'form':form,
        'data_series':data_series
    }
    return render_to_response('ihp_results/view_dsg_survey.html',context,RequestContext(request))



from scorecard_processor import models
from models import Attachment
import plugins

from django import forms
class ResponseXLSForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ('file',)


@login_required
def import_response(request, agency_id):
    agency = get_object_or_404(models.Entity, pk = agency_id)
    form = ResponseXLSForm
    attachment = Attachment(entity=agency)
    if request.POST:
        form = form(request.POST, request.FILES, instance=attachment)
        if form.is_valid():
            attachment = form.save()
            response_set = _import_response(attachment.file, agency, request.user)
            return HttpResponseRedirect(response_set.get_absolute_url())
    else:
        form = form(instance=attachment)
    return render_to_response('ihp_results/import_response.html', {'form':form}, RequestContext(request))

import xlrd
def _import_response(xls, agency, user):
    survey = xlrd.open_workbook(xls.path).sheet_by_name('Survey Tool')
    currency = survey.row(2)[3].value
    data_series = models.DataSeries.objects.get(name='2011')
    try:
        response_set = agency.responseset_set.get(data_series=data_series, survey=models.Survey.objects.get(name="Survey for agencies"))
    except:
        response_set = agency.responseset_set.create(survey=models.Survey.objects.get(name="Survey for agencies"))
        response_set.data_series.add(data_series)
    questions = dict([(q.identifier,q) for q in response_set.survey.get_questions()])
    responses = response_set.get_responses()
    tick_mode = False
    choice_map = dict([(i[1]._proxy____unicode_cast().lower(),i[0]) for i in plugins.AidTypes().choices])
    for row_num in xrange(7,survey.nrows):
        if row_num in [7,10,11,12,13,21,22] or row_num > 27:
            continue
        row = survey.row(row_num)
        try:
            section_name = str(row[0].value)
        except:
            section_name = None
        if section_name != '':
            section = section_name

        try:
            q_num = str(int(row[3].value))
        except:
            tick_mode = True

        value = row[6].value
        try:
            comment = row[7].value
        except:
            comment = None

        question = questions[q_num]
        if tick_mode:
            if value != '':
                key = row[4].value
                key = choice_map[key.strip().lower()]
                value = {'y':True,'n':False}.get(value.lower())
                response = responses.get(question)
                if response:
                    update = response.get_value()
                    if not isinstance(update,list):
                        update = []
                    if value:
                        update = update + [key]
                        update = set(update)
                    else:
                        update = set(update) - set([key])
                    value = list(update)
                    response = None
                else:
                    if value:
                        value = [key]
                    else:
                        value = []
                if not response and value:
                    response = response_set.response_set.create(question=question, respondant=user, current=True)
                    response.value = {'value':value}
                    response.save()
                    responses[question] = response
        else:
            if q_num != '10':
                response = responses.get(question)
                try:
                    value = int(value)
                except:
                    value = None
                if response and response.get_value() != value:
                    response = None
                if not response and value != None:
                    response = response_set.response_set.create(question=question, respondant=user, current=True)
                    if q_num != '9':
                        response.value = {'value':''.join([currency,str(value)])}
                    else:
                        response.value = {'value':value}
                    response.save()
                    responses[question] = response
        
        if comment:
            try:
                comment_q = questions[section]
            except:
                continue
            response = responses.get(comment_q)
            if response and response.get_value() != comment:
                response = None
            if not response:
                response = response_set.response_set.create(question=comment_q, respondant=user, current=True)
                response.value = {'value':comment}
                response.save()
    return response_set
