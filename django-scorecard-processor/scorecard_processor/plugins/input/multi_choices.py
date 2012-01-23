from django.forms import MultipleChoiceField, CheckboxSelectMultiple
from scorecard_processor.plugins import base, register

class MultiChoiceField(MultipleChoiceField):
    name = "Multiple choice"
    choices = (('example','Example'),)
    widget = CheckboxSelectMultiple

#register.register('input','Multi-choice field','multi_choice', MultiChoiceField)
