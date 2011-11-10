from scorecard_processor.plugins import base, register

class NumDenomPlugin(base.ProcessPlugin):
    name = 'Divide(Sum(Argument 1), Sum(Argument 2))'
    argument_list = ['numerator', 'denominator']

    def process_item(self, arguments):
        #TODO: handle NotApplicable
        ratio = arguments.denominator.get_value()
        if ratio > 0:
            ratio = arguments.numerator.get_value() / arguments.denominator.get_value() * 100
        return ratio

class OneMinusNumDenomPlugin(NumDenomPlugin):
    name = '100 - Divide(Sum(Argument 1), Sum(Argument 2))'
    def process_item(self, arguments):
        result = super(OneMinusNumDenomPlugin,self).process(arguments) 
        if result:
            return 100 - result

register.register('process','Unweighted operations','num_denom',NumDenomPlugin)
register.register('process','Unweighted operations','one_minus_num_denom',OneMinusNumDenomPlugin)
