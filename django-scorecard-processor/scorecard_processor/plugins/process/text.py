from scorecard_processor.plugins import base, register

def sum_values(x, y):
    return x + y

class Concat(base.ProcessPlugin):
    name = 'Concatenate responses'
    argument_list = ['response']

    def process(self):
        return base.Value("\n\n".join(self.get_arguments().response.get_values()))

register.register('process','Text','concat',Concat)
