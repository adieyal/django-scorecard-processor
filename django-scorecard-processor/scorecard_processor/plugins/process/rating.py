from scorecard_processor.plugins import base, register

class Rating(base.ProcessPlugin):
    name = 'Ratings'
    argument_list = ['percentage']
    input_type = base.Scalar
    output_type = base.Scalar

    def process(self):
        value = self.get_arguments().percentage
        if value == None:
            output = ''
        else:
            value = value.get_value()
            output = 'cross'
            if value > 50:
                output = 'dash'
            if value > 80:
                output = 'tick'
        return self.output_type(output)

register.register('process','Rating','rating',Rating)
