from django.forms import ChoiceField
from scorecard_processor.plugins import base, register

class YesNoNAField(ChoiceField):
    def __init__(self, *args, **kwargs):
        super(YesNoNAField,self).__init__(*args,**kwargs)
        self.choices = (
                ('yes','Yes'),
                ('no','No'),
                ('n/a','n/a'),
            )

register.register('input','Yes / No / N/A choice','yes_no_na_choice',YesNoNAField)
