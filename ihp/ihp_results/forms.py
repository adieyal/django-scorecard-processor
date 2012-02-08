from collections import defaultdict

from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify

from bootstrap.forms import *

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
        self.series = kwargs.pop('series')
        self.country = kwargs.pop('country')

        super(QuestionForm, self).__init__(*args, **kwargs)
        self.layout = []

        responsesets = self.entity.responseset_set.filter(data_series=self.country).filter(data_series__in=self.series) 
        response_dict = dict([(r.pk,r) for r in responsesets])
        responses = Response.objects.filter(
                        current=True,
                        response_set__in=responsesets).\
                    select_related('question')
        question_dict = defaultdict(list)

        for response in responses:
            #Limit db hits for responsesets
            response.response_set = response_dict[response.response_set_id]
            question_dict[response.question].append(response)

        for group in self.survey.questiongroup_set.all().select_related('question'):
            fieldset = QuestionFieldset(group)
            for question in group.question_set.all():
                label = True
                if question.question == "Voluntary additional information":
                    self.add_field_from_question(question, self.series[0])
                    fieldset.add_field('q_%s_%s' % (question.pk, self.series[0].pk))
                else:
                    for series in self.series:
                        self.add_field_from_question(question, series, label)
                        fieldset.add_field('q_%s_%s' % (question.pk, series.pk))
                        label = False
            self.layout.append(fieldset)

        #TODO:  get initial values
        #for series in self.series:
        #    self.initial.update(dict([
        #            ('q_%s' % response.question.pk, response.get_value()) 
        #            for response in self.entity.responseset_set.filter(current=True)
        #        ]))
            
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
        vomit
