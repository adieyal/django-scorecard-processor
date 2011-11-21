from collections import defaultdict

from django import forms
from bootstrap.forms import *
from models.inputs import ResponseSet, Response
from models.outputs import OperationArgument
from plugins import register


class QuestionFieldset(Fieldset):
    def __init__(self, question_group, *fields):
        self.legend_html = question_group and ('<legend>%s</legend>' % question_group.name) or ''
        if question_group and question_group.help_text:
            self.legend_html += "<p>%s</p>" % question_group.help_text
        self.fields = fields

class ResponseSetForm(forms.ModelForm):
    #TODO: Make django-bootstrap support modelforms
    # https://github.com/earle/django-bootstrap/issues/3
    class Meta:
        model = ResponseSet
        exclude = ('survey','entity','submission_date','last_update','respondant')

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
        fieldsets = defaultdict(list)
        general = []

        for question in self.survey.question_set.all():
            field = register.get_input_plugin(question.widget).plugin
            self.fields['q_%s' % question.pk] = field(
                        label='%s. %s' % (question.identifier,question.question),
                        help_text=question.help_text
            )
            if question.group:
                fieldsets[question.group].append('q_%s' % question.pk)
            else:
                general.append('q_%s' % question.pk)

        self.initial.update(dict([
                ('q_%s' % response.question.pk, response.value) 
                for response in self.instance.response_set.filter(current=True)
            ]))
            
        self.layout = [QuestionFieldset(key,*value) for key, value in fieldsets.items()]

        if general:
            self.layout.append(Fieldset('',*general))

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

            if instance and instance.get_value() != value:
                instance = None

            if not instance:
                instance = Response(
                    response_set = self.instance,
                    question = question,
                    value = value,
                    valid = True,
                    current = True
                )
                instance.save()

