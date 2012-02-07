from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify
from bootstrap.forms import *
from models.inputs import ResponseSet, Response, ResponseOverride
from models.outputs import OperationArgument
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

class QuestionForm(BootstrapForm):

    def __init__(self, *args, **kwargs):
        self.entity = kwargs.pop('entity')
        self.survey = kwargs.pop('survey')
        self.user = kwargs.pop('user')
        self.series = kwargs.pop('series')
        self.country = kwargs.pop('country')

        super(QuestionForm, self).__init__(*args, **kwargs)
        self.layout = []

        responsesets = survey.entity.responseset_set.filter(data_series=self.country).filter(data_series__in=self.series) 
        response_dict = dict([(r.pk,r) for r in responsesets])
        responses = Response.objects.filter(
                        active=True,
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
                for series in self.series:
                    self.add_field_from_question(question, series, label)
                    fieldset.add_field('q_%s_%s' % question.pk, series.pk)
                    label = False
            self.layout.append(fieldset)

        #TODO:  get initial values
        #for series in self.series:
        #    self.initial.update(dict([
        #            ('q_%s' % response.question.pk, response.get_value()) 
        #            for response in self.entity.responseset_set.filter(current=True)
        #        ]))
            
    def add_field_from_question(self, question, series, label):
        field = register.get_input_plugin(question.widget).plugin
        if label:
            label="""<span class="identifier">%s.</span> 
                     <span class="question">%s</span>""" % (question.identifier,question.question)
        else:
            label = ""
        self.fields['q_%s_%s' % (question.pk,series.pk)] = field(
                    help_text = question.help_text,
                    label = label,
                    required = False,
                    attrs = {'class':"series_%s" % series.pk}
        )

    def save(self):
        vomit
