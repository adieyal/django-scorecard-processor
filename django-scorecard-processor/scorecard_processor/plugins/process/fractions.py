from scorecard_processor.plugins import base, register

def sum_values(x, y):
    return x + y.get_value()

class NumDenomPlugin(base.ProcessPlugin):
    name = 'Divide(Sum(Argument 1), Sum(Argument 2))'
    argument_list = ['numerator', 'denominator']

    def process(self):
        #TODO: handle NotApplicable
        return base.Value(100 * (
                reduce(sum_values,arguments.numerator.get_value()) /
                reduce(sum_values,arguments.denominator.get_value()
            )))

class OneMinusNumDenomPlugin(NumDenomPlugin):
    name = '100 - Divide(Sum(Argument 1), Sum(Argument 2))'
    def process(self, arguments):
        result = super(OneMinusNumDenomPlugin,self).process(arguments) 
        if result:
            return base.Value(100 - result.get_value())

register.register('process','Unweighted operations','num_denom',NumDenomPlugin)
register.register('process','Unweighted operations','one_minus_num_denom',OneMinusNumDenomPlugin)