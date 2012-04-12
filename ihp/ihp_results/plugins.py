from django.utils.translation import ugettext_lazy as _
from scorecard_processor.plugins.input.multi_choices import register, MultiChoiceField
from scorecard_processor.plugins.input.choices import ChoiceField
from decimal import Decimal

class FourPointScale(ChoiceField):
    name = "Four point perfomance scale"
    def __init__(self, *args, **kwargs):
        super(FourPointScale,self).__init__(*args,**kwargs)
        self.choices = (
                ('',''),
                ('a','A'),
                ('b','B'),
                ('c','C'),
                ('d','D'),
            )

register.register('input','IHP field','four_point', FourPointScale)

class YesNoDevelopment(ChoiceField):
    name = "Yes/No/Under development"
    def __init__(self, *args, **kwargs):
        super(YesNoDevelopment,self).__init__(*args,**kwargs)
        self.choices = (
                ('',''),
                ('yes',_('Yes')),
                ('no',_('No')),
                ('under_development',_('Under development')),
            )

register.register('input','IHP field','yes_no_dev', YesNoDevelopment)

class AidTypes(MultiChoiceField):
    name = "Aid types"
    def __init__(self, *args, **kwargs):
        super(AidTypes,self).__init__(*args, **kwargs)
        self.choices = (
            ('financial',_('Financial support')),
            ('technical',_('Technical assistance (non-financial)')),
            ('lobbying',_('Lobbying/advocacy - non-financial')),
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
                     ('', ''),
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
                     ('NOK', _('Norwegian krone')),
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
