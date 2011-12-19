from scorecard_processor.plugins import base, register

class SingleValue(base.ProcessPlugin):
    name = 'Validate single value (y/n)'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar
    options = { 'value': basestring, 'match':basestring, 'miss':basestring }
    defaults = { 'value':'yes', 'match':'y', 'miss':'n' }

    def process(self):
        values = self.get_arguments().items.get_values()
        assert len(values) == 1
        if values[0].get_value().lower() == self.get_config('value'):
            return self.output_type(self.get_config('match'))
        return self.output_type(self.get_config('miss'))

class SingleValueInteger(SingleValue):
    name = 'Validate single value (100 / 0)'
    defaults = { 'value':'yes', 'match':100, 'miss':0 }

register.register('process','Assert value','assert_value_yn',SingleValue)
register.register('process','Assert value','assert_value_integer',SingleValueInteger)

class CombineValues(base.ProcessPlugin):
    name = 'Combine Values'
    argument_list = ['arg1','arg2']
    input_type = base.Vector
    output_type = base.Scalar
    options = { 'value': basestring }
    defaults = { 'value':'yes' }

    def process(self):
        output = []
        for values in [self.get_arguments().arg1.get_values(), self.get_arguments().arg2.get_values()]:
            for value in values:
                if value.get_value():
                    if value.get_value().lower() == self.get_config('value'):
                        return output.append('y')
                    else:
                        return output.append('y')
                else:
                    output.append(' ')
        return self.output_type(''.join(output))

register.register('process','Combine values','combine_values',CombineValues)
