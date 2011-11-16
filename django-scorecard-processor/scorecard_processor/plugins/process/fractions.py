from scorecard_processor.plugins import base, register

def sum_values(x, y):
    return x + y

class NumDenomPlugin(base.ProcessPlugin):
    name = 'Divide(Sum(Argument 1), Sum(Argument 2))'
    argument_list = ['numerator', 'denominator']

    def process(self):
        numerator = [float(x) for x in self.get_arguments().numerator.get_values()]
        denominator = [float(x) for x in self.get_arguments().denominator.get_values()]
        if numerator == [] or denominator == []:
            return 0
        return base.Value(100 * (
                reduce(sum_values, numerator) /
                reduce(sum_values, denominator)
            ))

class OneMinusNumDenomPlugin(NumDenomPlugin):
    name = '100 - Divide(Sum(Argument 1), Sum(Argument 2))'
    def process(self):
        result = super(OneMinusNumDenomPlugin,self).process() 
        if result:
            return base.Value(100 - result.get_values())
        return result

register.register('process','Unweighted operations','num_denom',NumDenomPlugin)
register.register('process','Unweighted operations','one_minus_num_denom',OneMinusNumDenomPlugin)
