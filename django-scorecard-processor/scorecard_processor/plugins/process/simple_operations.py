from scorecard_processor.plugins import base, register
import decimal

class Sum(base.ProcessPlugin):
    name = 'Sum items'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        values = [decimal.Decimal(item.get_value()) for item in self.get_arguments().items.get_values()]
        return self.output_type(reduce(lambda x,y: x + y, values))

register.register('process','Math','sum_items',Sum)
