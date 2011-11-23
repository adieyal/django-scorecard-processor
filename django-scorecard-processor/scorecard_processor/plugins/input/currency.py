from django.forms import DecimalField, CharField, TextInput
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode

from scorecard_processor.plugins import base, register

class CurrencyWidget(TextInput):
    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u"""<span class="currency"><span class="code">%s</span><span class="symbol">%s</span></span><input%s />""" % (self.currency[0],self.currency[1],flatatt(final_attrs)))

class FixedCurrency(DecimalField):
    widget = CurrencyWidget
    name = "Fixed Currency"
    currency = ('USD','$')

    def __init__(self, *args, **kwargs):
        if 'currency' in kwargs:
            self.currency = kwargs.pop('currency')

        super(FixedCurrency,self).__init__(*args,**kwargs)
        self.widget.currency = self.currency

    def to_python(self, value):
        if isinstance(value, basestring):
            value = value.replace(' ','') #strip spaces
            if len(value.split(',')[-1]) > 2:
                value = value.replace(',','')
        return super(FixedCurrency,self).to_python(value)
            

register.register('input','Currency field','fixed_currency', FixedCurrency)
