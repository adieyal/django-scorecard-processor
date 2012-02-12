from django.utils.translation import ugettext_lazy as _
from scorecard_processor.plugins.input.multi_choices import register, MultiChoiceField
from decimal import Decimal

class AidTypes(MultiChoiceField):
    name = "Aid types"
    def __init__(self, *args, **kwargs):
        super(AidTypes,self).__init__(*args, **kwargs)
        self.choices = (
            ('financial',_('Financial support')),
            ('technical',_('Technical assistance (non-financial)')),
            ('lobbying',_('Lobbying/advocay - non-financial'))
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
        'invalid_currency':_('Please choose a valid currency'),
        'invalid_value':_('Please enter a numeric amount')
    }

    def __init__(self, *args, **kwargs):
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        self.required = kwargs.get('required', False)
        localize = kwargs.get('localize', False)
        choices = (
                     ('USD', _('US Dollar')),
                     ('GBP', _('British Pound')),
                     ('EUR', _('Euro')),
                     ('AUD', _('Australian Dollar')),
                     ('SEK', _('Swedish Krona')),
                     ('XOF', _('CFA Franc BCEAO')),
                     ('BIF', _('Burundi Franc')),
                     ('DJF', _('Djibouti Franc')),
                     ('CDF', _('Congolese Franc')),
                     ('SVC', _('El Salvador Colon')),
                     ('ETB', _('Ethiopian Birr')),
                     ('MRO', _('Mauritanian Ouguiya')),
                     ('MZN', _('Mozambique New Metical')),
                     ('NPR', _('Nepal Rupee')),
                     ('NGN', _('Nigerian Naira')),
                     ('RWF', _('Rwandan Franc')),
                     ('SLL', _('Sierra Leone Leone')),
                     ('SDG', _('Sudanese Pound')),
                     ('UGX', _('Uganda Shilling')),
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
