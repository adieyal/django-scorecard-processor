from django import forms
from bootstrap.forms import *
from models.inputs import ResponseSet

class QuestionForm(forms.Form):
    #TODO: save responses / switch to save even if invalid
    model = ResponseSet
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        self.instance = kwargs.pop('instance')
        super(QuestionForm, self).__init__(*args, **kwargs)

        for question in self.survey.question_set.all():
            self.fields[question.identifier] = forms.CharField(
                        label=question.question
            )

    def save(self):
        for question in self.survey.question_set.all():
            value = self.cleaned_data[question.identifier]
            self.instance.response_set.create(
                question = question,
                value = value,
                valid = True
            )
