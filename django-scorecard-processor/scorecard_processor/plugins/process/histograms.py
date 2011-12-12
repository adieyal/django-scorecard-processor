from scorecard_processor.plugins import base, register

class Count(base.ProcessPlugin):
    name = 'Count'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        values = self.get_arguments().items.get_values()
        return self.output_type(len(values))

register.register('process','Count','count_items',Rating)
