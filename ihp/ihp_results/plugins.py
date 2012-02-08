from scorecard_processor.plugins.input.multi_choices import register, MultiChoiceField
from decimal import Decimal

class AidTypes(MultiChoiceField):
    name = "Aid types"
    def __init__(self, *args, **kwargs):
        super(AidTypes,self).__init__(*args, **kwargs)
        self.choices = (
            ('financial','Financial support'),
            ('technical','Technical assistance (non-financial)'),
            ('lobbying','Lobbying/advocay - non-financial')
        )
        self.widget.choices = self.choices

register.register('input','IHP field','aid_types', AidTypes)


from django.forms import MultiWidget, ChoiceField, Select, TextInput, MultiValueField, ValidationError

class CurrencyWidget(MultiWidget):
    def __init__(self, attrs=None, choices=None):
        if attrs == None:
            select_attrs = {'class':'medium'}
        else:
            select_attrs = attrs.copy()
            select_attrs['class'] = ' '.join([select_attrs.get('class',''),'small'])
        widgets = (Select(attrs=select_attrs, choices=choices),
                   TextInput(attrs=attrs))
        super(CurrencyWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value[0:3], Decimal(value[3:])]
        return ['','']

from scorecard_processor.plugins.input.currency import FixedCurrency

class CurrencySelector(MultiValueField):
    name = "Currency selector and input"
    widget = CurrencyWidget
    errors = {
        'invalid_currency':'Please choose a valid currency',
        'invalid_value':'Please enter a numeric amount'
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        self.required = kwargs.get('required', False)
        localize = kwargs.get('localize', False)
        choices = (
                     ('USD', 'US Dollar'),
                     ('GBP', 'British Pound'),
                     ('EUR', 'Euro'),
                     ('AUD', 'Australian Dollar'),
                     ('SEK', 'Swedish Krona'),
                     ('XOF', 'CFA Franc BCEAO'),
                     ('BIF', 'Burundi Franc'),
                     ('DJF', 'Djibouti Franc'),
                     ('CDF', 'Congolese Franc'),
                     ('SVC', 'El Salvador Colon'),
                     ('ETB', 'Ethiopian Birr'),
                     ('MRO', 'Mauritanian Ouguiya'),
                     ('MZN', 'Mozambique New Metical'),
                     ('NPR', 'Nepal Rupee'),
                     ('NGN', 'Nigerian Naira'),
                     ('RWF', 'Rwandan Franc'),
                     ('SLL', 'Sierra Leone Leone'),
                     ('SDG', 'Sudanese Pound'),
                     ('UGX', 'Uganda Shilling'),
                )
        fields = (
            ChoiceField(error_messages={'invalid': self.errors['invalid_currency']},
                      localize=localize, choices=choices, required=self.required),
            FixedCurrency(widget=TextInput,
                      error_messages={'invalid': self.errors['invalid_value']},
                      localize=localize, required=self.required),
        )
        if 'widget' not in kwargs:
            kwargs['widget'] = self.widget(choices=choices, attrs={'class':'currency_select medium'})
        super(CurrencySelector, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            if data_list[1] in [None, '']:
                if self.required:
                    raise ValidationError(self.errors['invalid_value'])
                return None
            return ''.join([unicode(d) for d in data_list]) 
        return ''


register.register('input','IHP field','multi_currency', CurrencySelector)
