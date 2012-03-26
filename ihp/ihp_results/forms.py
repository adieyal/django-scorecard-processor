from collections import defaultdict
from ordereddict import OrderedDict

from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

from bootstrap.forms import *

from scorecard_processor.models.meta import DataSeries
from scorecard_processor.models.inputs import ResponseSet, Response, ResponseOverride
from scorecard_processor.models.outputs import OperationArgument

from plugins import register

class QuestionFieldset(Fieldset):
    def __init__(self, question_group, *fields):
        self.legend_html = question_group and ('<legend>%s</legend>' % question_group.i18n.name) or ''
        self.div_id = question_group and 'qg_'+slugify(question_group.pk);
        if not self.div_id:
            self.div_id = 'general'
        
        if question_group and question_group.help_text:
            self.legend_html += "<p class='legend'>%s</p>" % question_group.i18n.help_text
        self.fields = list(fields)

    def add_field(self, field):
        self.fields.append(field)

    def render_fields(self, form):
        fields = []
        for field in self.fields:
            if isinstance(field, dict):
                question = field['question']
                label="""<span class="identifier">%s.</span> 
                     <span class="question">%s</span>""" % (question.i18n.identifier,question.i18n.question)
                fields.append("""<div class='question_group row'>
                                    <label class="question">%s</label>
                                    %s
                                </div>""" % (label, form.render_fields(field['fields'])))
            else:
                fields.append(form.render_fields([field]))
        return ''.join(fields)

    def as_html(self, form):
        return u"<div class='tab-pane' id='%s'><fieldset>%s<div class='fields'>%s</div></fieldset></div>" % (self.div_id, self.legend_html, self.render_fields(form))

import plugins

class MultiYearDataException(Exception):
    pass

class QuestionForm(BootstrapForm):

    currency = forms.ChoiceField(
                    choices=plugins.CurrencySelector().widget.widgets[0].choices,
                    label=_("Currency"),
                    help_text=_("Please select your currency")
                ) 
    baseline_year = forms.ChoiceField(
                        choices=((2005, 2005), (2006,2006), (2007,2007)),
                        label=_("Baseline data"),
                    ) 
    current_year = forms.ChoiceField(
                        choices=((2011,2011), (2010,2010)),
                        label=_("Latest data"),
                    ) 

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        self.survey = kwargs.pop('survey')
        self.user = kwargs.pop('user')
        self.series = OrderedDict([(s.pk,s) for s in kwargs.pop('series')])
        self.country = kwargs.pop('country')
        self.collection_year = {}
        try:
            self.static = kwargs.pop('static')
        except KeyError:
            self.static = False

        super(QuestionForm, self).__init__(*args, **kwargs)
        self.layout = []

        self.responsesets = list(self.entity.responseset_set.filter(data_series=self.country).filter(data_series__in=self.series.values()))
        response_dict = dict([(r.pk,r) for r in self.responsesets])
        self.response_types = dict([(r.get_data_series_by_type()['Data collection year'],r) for r in self.responsesets])
        self.responses = Response.objects.filter(
                        current=True,
                        response_set__in=self.responsesets).\
                    select_related('question')
        self.question_dict = defaultdict(dict)
        self.questions = {}
        self.response = {}

        if self.static:
            for fieldname in ['currency','baseline_year','current_year']:
               field = self.fields[fieldname]
               field.widget.attrs['readonly'] = 'readonly'
               field.widget.attrs['disabled'] = 'disabled'
               field.widget.attrs['class'] = 'hidden'
               field.required = False
            

        collection_lookup = {"Baseline":"baseline_year","2012 collection":"current_year"}
        for responseset in self.responsesets:
            currency = responseset.get_meta('currency')
            if currency and not self.initial.get('currency'):
                self.initial['currency'] = currency['value']

            ds_dict = responseset.get_data_series_by_type()
            if ds_dict['Data collection year'] not in self.collection_year:
                self.collection_year[ds_dict['Data collection year']] = ds_dict['Year']
                field = self.fields[collection_lookup[ds_dict['Data collection year'].name]]
                field.widget.attrs['readonly'] = 'readonly'
                field.widget.attrs['disabled'] = 'disabled'
                field.required = False
            else:
                if self.collection_year[ds_dict['Data collection year']] != ds_dict['Year']:
                    raise MultiYearDataException

        for response in self.responses:
            #Limit db hits for responsesets
            response.response_set = response_dict[response.response_set_id]
            ds_dict = response.response_set.get_data_series_by_type()
            self.question_dict[response.question][ds_dict['Data collection year']]=response

        for collection, year in self.collection_year.items():
            self.initial[collection_lookup[collection.name]] = year.name
            rs = self.response_types.get(collection)
            if rs and (rs.editable == False or self.static):
               field = self.fields[collection_lookup[collection.name]]
               field.widget.attrs['readonly'] = 'readonly'
               field.widget.attrs['disabled'] = 'disabled'
               field.widget.attrs['class'] = 'hidden'
               field.required = False

        series_list = self.series.values()
        current_series = series_list[0]
        series_list.reverse()

        for group in self.survey.questiongroup_set.all().select_related('question'):
            fieldset = QuestionFieldset(group)
            for question in group.question_set.all():
                label = True
                self.questions[question.pk] = question
                if question.widget == 'textbox':
                    self.add_field_from_question(question, current_series)
                    fieldset.add_field('q_%s_%s' % (question.pk, current_series.pk))
                else:
                    fields = []
                    for series in series_list:
                        rs = self.response_types.get(series)
                        self.add_field_from_question(question, series, False)
                        fields.append('q_%s_%s' % (question.pk, series.pk))
                    fieldset.add_field({'question':question, 'fields':fields})
            self.layout.append(fieldset)

        for question, series in self.question_dict.items():
            for ds, response in series.items():
                self.initial['q_%s_%s' % (response.question.pk, ds.pk)] = response.get_value()
                self.response['q_%s_%s' % (response.question.pk, ds.pk)] = response
            
    def add_field_from_question(self, question, series, label=True):
        read_only = self.static
        rs = self.response_types.get(series)
        if rs and rs.editable == False:
            read_only=True
        field = register.get_input_plugin(question.widget).plugin
        if label:
            label="""<span class="identifier">%s.</span> 
                     <span class="question">%s</span>""" % (question.i18n.identifier,question.i18n.question)
        else:
            label = {
                    "Baseline":_("Baseline data"),
                    "2012 collection":_("Latest data"),
                }.get(series.name)
        field = field(
                    help_text = question.i18n.help_text,
                    label = label,
                    required = False,
        )
        if read_only:
            field.widget.attrs['readonly'] = 'readonly'
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['class'] = 'hidden'
        self.fields['q_%s_%s' % (question.pk,series.pk)] = field

    def save(self):
        baseline_year = self.cleaned_data['baseline_year'] 
        if baseline_year:
            baseline_year = DataSeries.objects.get(name=baseline_year)
        else:
            baseline_year = None
        current_year = DataSeries.objects.get(name=self.cleaned_data['current_year'])
        currency = self.cleaned_data['currency']
        for responseset in self.responsesets:
            if responseset.editable:
                responseset.set_meta('currency',{'value':currency})

        del self.cleaned_data['currency']
        del self.cleaned_data['current_year']
        del self.cleaned_data['baseline_year']
        for key, value in self.cleaned_data.items():
            if value or key in self.response:
                # Check for existing response
                if key in self.response:
                    if  self.response[key].get_value() != value and self.response[key].response_set.editable:
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
                        if series.name == 'Baseline':
                            responseset.data_series.add(baseline_year)
                        else:
                            responseset.data_series.add(current_year)
                        self.responsesets.append(responseset)
                        responseset.set_meta('currency',{'value':currency})


                    if responseset.editable:
                        r = responseset.response_set.create(question=question, respondant=self.user, valid=True, current=True)
                        r.value = {'value':value}
                        r.save()
