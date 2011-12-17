from scorecard_processor.plugins import base, register

class SingleValue(base.ProcessPlugin):
    name = 'Validate single value'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar
    options = { 'value': basestring }
    defaults = { 'value':'yes' }

    def process(self):
        values = self.get_arguments().items.get_values()
        assert len(values) == 1
        if values[0].get_value().lower() == self.get_config('value'):
            return self.output_type('y')
        return self.output_type('n')

register.register('process','Assert value','assert_value',SingleValue)