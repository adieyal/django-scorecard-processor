from django import forms
from bootstrap.forms import *
from models.inputs import ResponseSet, Response

class ResponseSetForm(forms.ModelForm):
    #TODO: Make django-bootstrap support modelforms
    # https://github.com/earle/django-bootstrap/issues/3
    class Meta:
        model = ResponseSet
        exclude = ('survey','entity','submission_date','last_update','respondant')

class QuestionForm(BootstrapForm):
    #TODO: save responses / switch to save even if invalid
    #TODO: load initial values from self.instance into form fields
    #TODO: take a user object to save with each field update
        
    model = ResponseSet
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        self.instance = kwargs.pop('instance')
        super(QuestionForm, self).__init__(*args, **kwargs)

        for question in self.survey.question_set.all():
            self.fields['q_%s' % question.pk] = forms.CharField(
                        label='%s. %s' % (question.identifier,question.question),
                        help_text=question.help_text
            )

        self.initial.update(dict([
                ('q_%s' % response.question.pk, response.value) 
                for response in self.instance.response_set.filter(current=True)
            ]))
            
        #TODO: group question fields
        self.layout = (Fieldset("Monetary aid",*[key for key in self.fields.keys()]),)
          

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

