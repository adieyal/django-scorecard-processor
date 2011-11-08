import base
from register import register

class NumDenomPlugin(base.Plugin):
    name = 'Fraction'
    argument_list = ['numerator', 'denominator']

    def process_item(self, arguments):
        #TODO: handle NotApplicable
        ratio = arguments.denominator.get_value()
        if ratio > 0:
            ratio = arguments.numerator.get_value() / arguments.denominator.get_value() * 100
        return ratio

class OneMinusNumDenomPlugin(NumDenomPlugin):
    name = 'One minus fraction'
    def process_item(self, arguments):
        result = super(OneMinusNumDenomPlugin,self).process(arguments) 
        if result:
            return 100 - result

register('Scorecard operations','num_denom',NumDenomPlugin)
register('Scorecard operations','one_minus_num_denom',OneMinusNumDenomPlugin)
