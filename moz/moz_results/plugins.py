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
            ('lobbying',_('Lobbying/advocay - non-financial')),
            ('other',_('Other (please specify in Voluntary additional information)'))
        )
        self.widget.choices = self.choices

register.register('input','IHP field','aid_types', AidTypes)

class RepresentedTypes(MultiChoiceField):
    name = "CSO Representation Types"
    def __init__(self, *args, **kwargs):
        super(RepresentedTypes,self).__init__(*args, **kwargs)
        self.choices = (
            ("maternal",_("Maternal Health")),
            ("child",_("Child Health")),
            ("maleria",_("Malaria")),
            ("hiv",_("HIV/AIDS")),
            ("tb",_("TB")),
            ("systems",_("Health Systems Strengthening (Governance, Financing, HRH, Information Systems, Medicines, service delivery)")),
            ("nutrition",_("Nutrition")),
            ("international",_("International NGO")),
            ("national",_("National NGO")),
            ("failth",_("Faith Based Organisation")),
            ("umbrella",_("Umbrella Organisation")),
            ("professional",_("Professional Association")),

        )
        self.widget.choices = self.choices

register.register('input','IHP field','rep_types', RepresentedTypes)

class CSOInvolvement(MultiChoiceField):
    name = "CSO Involvement"
    def __init__(self, *args, **kwargs):
        super(CSOInvolvement,self).__init__(*args, **kwargs)
        self.choices = (
            ("joint_review",_("Joint Annual Reviews")),
            ("monthly",_("Monthly/quarterly coordination meetings")),
            ("thematic",_("Thematic working groups")),
            ("budget",_("Budget development / resource allocation")),
        )
        self.widget.choices = self.choices

register.register('input','IHP field','cso_involved', CSOInvolvement)


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

conversions = {
    "BRL": 0.6,
    "GBP": 1.6,
    "CAD": 1.01,
    "EUR": 1.39,
    "DKK": 0.19,
    "JPY": 0.01,
    "MZN": 0.03,
    "NOK": 0.18,
    "SEK": 0.15,
    "CHF": 1.13,
}
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
                     ("BRL", "Brazilian Real"),
                     ("CAD", "Canadian Dollar"),
                     ("DKK", "Danish Krone"),
                     ("JPY", "Japanese Yen"),
                     ("NOK", "Norwegian Kroner"),
                     ("SEK", "Swedish Krona"),
                     ("CHF", "Swiss Francs"),
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

    def get_calculated_value(self, data, currency = 'USD'):
        currency = data['value'][0:3]
        value = data['value'][3:]
        if currency != 'USD':
            return float(value)*conversions[currency]
        return value


register.register('input','IHP field','multi_currency', CurrencySelector)
