from collections import defaultdict
from ordereddict import OrderedDict

from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify

from bootstrap.forms import *

from scorecard_processor.models.meta import DataSeries
from scorecard_processor.models.inputs import ResponseSet, Response, ResponseOverride
from scorecard_processor.models.outputs import OperationArgument

from plugins import register

class QuestionFieldset(Fieldset):
    def __init__(self, question_group, *fields):
        self.legend_html = question_group and ('<legend>%s</legend>' % question_group.name) or ''
        self.div_id = question_group and 'qg_'+slugify(question_group.pk);
        if not self.div_id:
            self.div_id = 'general'
        
        if question_group and question_group.help_text:
            self.legend_html += "<p class='legend'>%s</p>" % question_group.help_text
        self.fields = list(fields)

    def add_field(self, field):
        self.fields.append(field)

    def as_html(self, form):
        return u"<div class='tab' id='%s'><fieldset>%s<div class='fields'>%s</div></fieldset></div>" % (self.div_id, self.legend_html, form.render_fields(self.fields))

import plugins

class MultiYearDataException(Exception):
    pass

class QuestionForm(BootstrapForm):

    currency = forms.ChoiceField(
                    choices=plugins.CurrencySelector().widget.widgets[0].choices,
                    label="Currency",
                    help_text="Please select your currency"
                ) 
    baseline_year = forms.ChoiceField(
                        choices=((2005, 2005), (2006,2006), (2007,2007)),
                        label="Baseline year",
                    ) 
    current_year = forms.ChoiceField(
                        choices=((2010,2010), (2011,2011)),
                        label="Current year",
                    ) 

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        self.survey = kwargs.pop('survey')
        self.user = kwargs.pop('user')
        self.series = OrderedDict([(s.pk,s) for s in kwargs.pop('series')])
        self.country = kwargs.pop('country')
        self.collection_year = {}

        super(QuestionForm, self).__init__(*args, **kwargs)
        self.layout = []

        self.responsesets = list(self.entity.responseset_set.filter(data_series=self.country).filter(data_series__in=self.series.values()))
        response_dict = dict([(r.pk,r) for r in self.responsesets])
        self.responses = Response.objects.filter(
                        current=True,
                        response_set__in=self.responsesets).\
                    select_related('question')
        self.question_dict = defaultdict(dict)
        self.questions = {}
        self.response = {}

        for response in self.responses:
            #Limit db hits for responsesets
            response.response_set = response_dict[response.response_set_id]
            ds_dict = dict([(d.group.name, d) for d in response.response_set.get_data_series()])
            self.question_dict[response.question][ds_dict['Data collection year']]=response
            if ds_dict['Data collection year'] not in self.collection_year:
                self.collection_year[ds_dict['Data collection year']] = ds_dict['Year']
            else:
                if self.collection_year[ds_dict['Data collection year']] != ds_dict['Year']:
                    raise MultiYearDataException

        collection_lookup = {"Baseline":"baseline_year","2012 collection":"current_year"}
        for collection, year in self.collection_year.items():
            self.initial[collection_lookup[collection.name]] = year.name

        for group in self.survey.questiongroup_set.all().select_related('question'):
            fieldset = QuestionFieldset(group)
            for question in group.question_set.all():
                label = True
                self.questions[question.pk] = question
                if question.question == "Voluntary additional information":
                    self.add_field_from_question(question, self.series.values()[0])
                    fieldset.add_field('q_%s_%s' % (question.pk, self.series.values()[0].pk))
                else:
                    for series in self.series.values():
                        self.add_field_from_question(question, series, label)
                        fieldset.add_field('q_%s_%s' % (question.pk, series.pk))
                        label = False
            self.layout.append(fieldset)

        for question, series in self.question_dict.items():
            for ds, response in series.items():
                self.initial['q_%s_%s' % (response.question.pk, ds.pk)] = response.get_value()
                self.response['q_%s_%s' % (response.question.pk, ds.pk)] = response
            
    def add_field_from_question(self, question, series, label=True):
        field = register.get_input_plugin(question.widget).plugin
        if label:
            label="""<span class="identifier">%s.</span> 
                     <span class="question">%s</span>""" % (question.identifier,question.question)
        else:
            label = series.name
        field = field(
                    help_text = question.help_text,
                    label = label,
                    required = False,
        )
        self.fields['q_%s_%s' % (question.pk,series.pk)] = field

    def save(self):
        baseline_year = DataSeries.objects.get(name=self.cleaned_data['baseline_year'])
        current_year = DataSeries.objects.get(name=self.cleaned_data['current_year'])
        currency = self.cleaned_data['currency']

        del self.cleaned_data['currency']
        del self.cleaned_data['current_year']
        del self.cleaned_data['baseline_year']
        for key, value in self.cleaned_data.items():
            if value:
                # Check for existing response
                if key in self.response and self.response[key] != value:
                    instance = Response(
                        response_set = self.response[key].response_set,
                        respondant = self.user,
                        question = self.response[key].question,
                        valid = True,
                        current = True
                    )
                    instance.value = {'value':value}
                    instance.save()
                else:
                    q, q_id, s_id = key.split('_')
                    question = self.questions[int(q_id)]
                    series = self.series[int(s_id)]

                    responseset = None
                    for rs in self.responsesets:
                        if set(rs.get_data_series()) == set([baseline_year, self.country, series]):
                            responseset = rs
                            break
                        elif set(rs.get_data_series()) == set([current_year, self.country, series]):
                            responseset = rs
                            break

                    if responseset == None:
                        responseset = ResponseSet(
                            survey=self.survey,
                            entity=self.entity
                        )
                        responseset.save()
                        responseset.data_series.add(self.country)
                        responseset.data_series.add(series)
                        print(series.name)
                        if series.name == 'Baseline':
                            responseset.data_series.add(baseline_year)
                        else:
                            responseset.data_series.add(current_year)
                        self.responsesets.append(responseset)

                    r = responseset.response_set.create(question=question, respondant=self.user, valid=True, current=True)
                    r.value = {'value':value}
                    r.save()
