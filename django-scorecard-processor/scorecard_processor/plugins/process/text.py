from scorecard_processor.plugins import base, register

def sum_values(x, y):
    return x + y

class Concat(base.ProcessPlugin):
    name = 'Concatenate responses'
    argument_list = ['response']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        return self.output_type("\n\n".join([v.get_value() for v in self.get_arguments().response.get_values()]))

register.register('process','Text','concat',Concat)
