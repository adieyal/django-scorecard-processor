from scorecard_processor.plugins import base, register
import decimal

class Sum(base.ProcessPlugin):
    name = 'Sum items'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        values = []
        for item in self.get_arguments().items.get_values():
            value = item.get_value()
            if value:
                try:
                    values.append(decimal.Decimal(value))
                except decimal.InvalidOperation:
                    pass
        if len(values)>1:
            return self.output_type(reduce(lambda x,y: x + y, values))
        if len(values)==1:
            return self.output_type(values[0])
        return self.output_type(0)

register.register('process','Math','sum_items',Sum)
