from scorecard_processor.plugins import base, register

class Sum(base.ProcessPlugin):
    name = 'Sum items'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        values = self.get_arguments().items.get_values()
        return self.output_type(reduce(lambda x,y: x.get_value() + y, values))

register.register('process','Math','sum_items',Sum)
