import decimal 
from scorecard_processor.plugins import base, register

class Count(base.ProcessPlugin):
    name = 'Count'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        values = self.get_arguments().items.get_values()
        return self.output_type(len(values))

class CountValue(Count):
    name = "Frequency of keyword (%)"
    options = {
        'value':basestring,
        'decimal_places':int,
        'ignore':list
    }
    defaults = {
        'decimal_places':1,
        'value':'yes',
        'ignore':['n/a']
    }

    def process(self):
        items = self.get_arguments().items.get_values()
        count = len([item for item in items if item.get_value().lower() not in self.get_config('ignore')])
        if count == 0:
            return None
        count_values = len(filter(lambda x: x.get_value().lower() == self.get_config('value'),items))

        places = self.get_config('decimal_places')
        if places>0:
            quant = decimal.Decimal('.'.join(['1','0'*places]))
        else:
            quant = decimal.Decimal('1')

        return self.output_type((decimal.Decimal(count_values) / count * 100).quantize(quant))


register.register('process','Count','count_items',Count)
register.register('process','Count','keyword_frequency',CountValue)
