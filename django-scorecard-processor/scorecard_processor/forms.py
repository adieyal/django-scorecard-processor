from django import forms
from bootstrap.forms import *
from models.inputs import ResponseSet

class QuestionForm(BootstrapForm):
    #TODO: save responses / switch to save even if invalid
    #TODO: load initial values from self.instance into form fields
        
    model = ResponseSet
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        self.instance = kwargs.pop('instance')
        super(QuestionForm, self).__init__(*args, **kwargs)

        for question in self.survey.question_set.all():
            self.fields[question.identifier] = forms.CharField(
                        label=question.question
            )
        #TODO: group question fields
        self.layout = (Fieldset("Default",*[key for key in self.fields.keys()]),)
          

    def save(self):
        if not self.instance.pk:
            self.instance.save()
        for question in self.survey.question_set.all():
            value = self.cleaned_data[question.identifier]
            # Only create a new 'response' if the existing response is
            # different
            self.instance.response_set.get_or_create(
                question = question,
                value = value,
                valid = True,
                current = True
            )
