# -*- coding: utf-8 -*-
# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import DetailView, ListView, DeleteView, CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils import translation
from django import http
from django.views.decorators.csrf import requires_csrf_token
from django.template import Context, RequestContext, loader


from guardian.shortcuts import get_perms, assign, remove_perm, get_objects_for_user


from scorecard_processor.models import Entity, DataSeriesGroup, Survey, DataSeries
from plugins import MultiChoiceField, CurrencySelector

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

@requires_csrf_token
def exception_handler(request):
    t = loader.get_template('500.html')
    context = {}
    if hasattr(request,'problem'):
        context['problem'] = request.problem
    return http.HttpResponseServerError(t.render(Context(context)))



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
            try:
                response_set = _import_response(attachment.file, agency, request.user)
            except MyImportError, e:
                request.problem = e
                raise e
            return HttpResponseRedirect(reverse('survey_dsg_response_view',args=[str(agency.pk),'Country', str(response_set.survey.pk), response_set.get_data_series_by_type()['Country'].name]))
    else:
        form = form(instance=attachment)
    return render_to_response('ihp_results/import_response.html', {'form':form}, RequestContext(request))

class MyImportError(Exception):
    pass

import xlrd
def _import_response(xls, agency, user):
    fr_config = None
    try:
        response = xlrd.open_workbook(xls.path).sheet_by_name('Survey Tool')
    except xlrd.XLRDError:
        response = None

    if not response:
        try:
            response = xlrd.open_workbook(xls.path).sheet_by_name('Questionnaire')
        except xlrd.XLRDError:
            response = None 
        if response:
            fr_config = config['gov_fr']

    if not response:
        try:
            response = xlrd.open_workbook(xls.path).sheet_by_name('questionnaire')
        except xlrd.XLRDError:
            response = None 
        if response:
            fr_config = config['gov_fr']

    if not response:
        raise MyImportError("Couldn't find a sheet named 'Survey Tool', 'Questionnaire' or 'questionnaire'")

    if response.row(7)[0].value == '1DP':
        return _process_response(xls, agency, user, response, config=config["dp"])
    else:
        if fr_config:
            return _process_response(xls, agency, user, response, config=fr_config)
        else:
            return _process_response(xls, agency, user, response, config=config["gov"])

config = {
    'gov':{
        'survey':'2012 Survey for Governments',
        'currency':(1,2),
        'country':(0,2),
        'baseline_year':(2,2),
        'latest_year':(3,2),
        'start_row':7,
        'question_column':2,
        'baseline_column':4,
        'current_column':5,
        'comment_column':6,
        'choice_column':3,
        'skip_rows':[]
    },
    'gov_fr':{
        'survey':'2012 Survey for Governments',
        'currency':(1,1),
        'country':(0,1),
        'baseline_year':(2,1),
        'latest_year':(3,1),
        'start_row':6,
        'question_column':1,
        'baseline_column':3,
        'current_column':4,
        'comment_column':5,
        'choice_column':2,
        'skip_rows':[]
    },
    'dp':{
        'survey':'2012 Survey for Agencies',
        'currency':(2,3),
        'country':(0,3),
        'baseline_year':(3,3),
        'latest_year':(4,3),
        'start_row':7,
        'question_column':3,
        'baseline_column':5,
        'current_column':6,
        'comment_column':7,
        'choice_column':4,
        'skip_rows':[]
    },
}


def _process_response(xls, agency, user, submission, config):
    survey = models.Survey.objects.get(name=config['survey'])
    currency = submission.cell(*config['currency']).value[:3]
    country = submission.cell(*config['country']).value
    french = submission.cell(config['start_row']-1,0).value.lower() == u"n° indicateur"
    if french:
        translation.activate('fr')

    try:
        baseline_year = models.DataSeries.objects.get(name=unicode(submission.cell(*config['baseline_year']).value)[:4])
    except:
        baseline_year = None
    try:
        current_year = models.DataSeries.objects.get(name=unicode(submission.cell(*config['latest_year']).value)[:4])
    except DataSeries.DoesNotExist:
        raise MyImportError("Can't find a valid year, Please check the drop downs.")

    if baseline_year:
        try:
            data_series = [
                baseline_year,
                models.DataSeries.objects.get(name=country),
                models.DataSeries.objects.get(name="Baseline"),
            ]
        except DataSeries.DoesNotExist:
            raise MyImportError("Couldn't find a valid country, please check drop downs") 
        baseline = agency.get_response_set(data_series=data_series, survey=survey)
        if not baseline:
            baseline = agency.responseset_set.create(survey=survey)
            for ds in data_series:
                baseline.data_series.add(ds)
    else:
        baseline = None


    data_series = [
        current_year,
        models.DataSeries.objects.get(name=country),
        models.DataSeries.objects.get(name="2012 collection"),
    ]
    current = agency.get_response_set(data_series=data_series, survey=survey)
    if not current:
        current = agency.responseset_set.create(survey=survey)
        for ds in data_series:
            current.data_series.add(ds)

    for responseset in baseline, current:
        if responseset and responseset.editable:
            responseset.set_meta('currency',{'value':currency})


    questions = dict([(q.identifier,q) for q in survey.get_questions()])
    if baseline:
        baseline_responses = baseline.get_responses()
    else:
        baseline_responses = {}
    current_responses = current.get_responses()
    tick_mode = False
#    choice_map = dict([(i[1]._proxy____unicode_cast().lower(),i[0]) for i in plugins.AidTypes().choices])
    for row_num in xrange(config['start_row'],submission.nrows):
        if row_num in config['skip_rows']:
            continue

        row = submission.row(row_num)
        try:
            section_name = str(row[0].value)
        except:
            section_name = None
        if section_name != '':
            section = section_name

        try:
            q_num = str(int(row[config['question_column']].value))
        except:
            tick_mode = True
        else:
            tick_mode = False

        baseline_value = row[config['baseline_column']].value
        current_value = row[config['current_column']].value
        try:
            comment = row[config['comment_column']].value
        except:
            comment = None

        question = questions[q_num]

        iterate = [(current_value, current_responses, current)]
        if baseline:
            iterate.append((baseline_value, baseline_responses, baseline))

        for value, responses, response_set in iterate:
            if tick_mode:
                choice_map = dict([(i[1]._proxy____unicode_cast().lower(),i[0]) for i in question.plugin.plugin().choices])
                if value != '':
                    key = row[config['choice_column']].value
                    try:
                        key = choice_map[key.strip().lower()]
                    except KeyError:
                        continue
                    value = {'y':True,'n':False,'qui':True,'oui':True,'non':False}.get(value.lower())
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
                if not isinstance(question.plugin.plugin, MultiChoiceField):
                    response = responses.get(question)

                    if isinstance(question.plugin.plugin(), CurrencySelector):
                        if isinstance(value, basestring):
                            value = value.replace(' ','') #strip spaces
                            if len(value.split(',')[-1]) > 2:
                                value = value.replace(',','')

                    if isinstance(value,basestring) and value.lower() in ['qui','oui','non']:
                        value = {'qui':'yes','oui':'yes', 'non':'no'}[value.lower()]

                    if isinstance(value,basestring) and value.lower() in ['yes','no']:
                        value = value.lower()
                    else:
                        try:
                            value = int(value)
                        except:
                            value = None

                    if value!=None and isinstance(question.plugin.plugin(), CurrencySelector):
                        value = ''.join([currency,str(value)])

                    if response and response.get_value() != value:
                        response = None
                    if not response and value != None:
                        response = response_set.response_set.create(question=question, respondant=user, current=True)
                        response.value = {'value':value}
                        response.save()
                        responses[question] = response
        
        if comment:
            try:
                comment_q = questions[section]
            except:
                continue
            response = current_responses.get(comment_q)
            if response and response.get_value() != comment:
                response = None
            if not response:
                response = current.response_set.create(question=comment_q, respondant=user, current=True)
                response.value = {'value':comment}
                response.save()
    return response_set

