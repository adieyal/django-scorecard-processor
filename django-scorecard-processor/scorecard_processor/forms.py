from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify
from bootstrap.forms import *
from models.inputs import ResponseSet, Response
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

class ResponseSetForm(forms.ModelForm):
    #TODO: Make django-bootstrap support modelforms
    # https://github.com/earle/django-bootstrap/issues/3
    class Meta:
        model = ResponseSet
        exclude = ('survey','entity','submission_date','last_update','respondant')

    def _get_responseset(self, survey, data_series):
        qs = self.Meta.model.objects.filter(survey=survey)
        #response = self.Meta.model.objects.get(survey=instance.survey, data_series__exact=self.cleaned_data['data_series'])
        for ds in data_series:
            qs = qs.filter(data_series=ds)
        try:
            response = qs.get()
        except self.Meta.model.DoesNotExist:
            response = None
        return response

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit',True)
        kwargs['commit'] = False
        instance = super(ResponseSetForm, self).save(*args,**kwargs)
        response = self._get_responseset(instance.survey, self.cleaned_data['data_series'])
        if response:
            return response
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class ArgumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArgumentForm, self).__init__(*args, **kwargs)
        # key should be your sortable-field - in your exaple it's *index*
        self.fields['position'].widget = forms.HiddenInput()
        self.fields['position'].label = ''

    class Meta:
        model = OperationArgument

class QuestionForm(BootstrapForm):
    #TODO: save responses / switch to save even if invalid
    #TODO: take a user object to save with each field update
        
    model = ResponseSet
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        self.instance = kwargs.pop('instance')
        super(QuestionForm, self).__init__(*args, **kwargs)
        general = []
        self.layout = []

        for group in self.survey.questiongroup_set.all().select_related('question'):
            fieldset = QuestionFieldset(group)
            for question in group.question_set.all():
                self.add_field_from_question(question)
                fieldset.add_field('q_%s' % question.pk)
            self.layout.append(fieldset)

        general = self.survey.question_set.filter(group=None)
        if general:
            questions = []
            for question in general:
                self.add_field_from_question(question)
                questions.append('q_%s' % question.pk)
            self.layout.append(Fieldset('',*questions))

        self.initial.update(dict([
                ('q_%s' % response.question.pk, response.get_value()) 
                for response in self.instance.response_set.filter(current=True)
            ]))
            
    def add_field_from_question(self, question):
        field = register.get_input_plugin(question.widget).plugin
        self.fields['q_%s' % question.pk] = field(
                    label="""<span class="identifier">%s.</span> 
                            <span class="question">%s</span>""" % (question.identifier,question.question),
                    help_text=question.help_text,
                    required=False
        )

    def save(self):
        if not self.instance.pk:
            self.instance.save()
        for question in self.survey.question_set.all():
            value = self.cleaned_data['q_%s' % question.pk]
            # Only create a new 'response' if the existing response is
            # different
            try:
                instance = self.instance.response_set.get(
                    question = question,
                    current = True
                )
            except Response.DoesNotExist:
                instance = None

            if not value and not instance:
                continue

            if instance and instance.get_value() != value:
                instance = None

            if not instance:
                instance = Response(
                    response_set = self.instance,
                    question = question,
                    valid = True,
                    current = True
                )
                instance.value = {'value':value}
                instance.save()

