from scorecard_processor.plugins import base, register
import decimal

def sum_values(x, y):
    return x + y

class NumDenomPlugin(base.ProcessPlugin):
    name = 'Divide(Sum(Argument 1), Sum(Argument 2))'
    argument_list = ['numerator', 'denominator']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        numerator = [float(x) for x in self.get_arguments().numerator.get_values()]
        denominator = [float(x) for x in self.get_arguments().denominator.get_values()]
        if numerator == [] or denominator == []:
            return None
        numerator = decimal.Decimal(str(reduce(sum_values, numerator)))
        denominator = decimal.Decimal(str(reduce(sum_values, denominator)))
        if denominator == 0:
            return None
        quant = decimal.Decimal('1.00')
        return self.output_type((100 * (
                numerator / 
                denominator
            )).quantize(quant))

class OneMinusNumDenomPlugin(NumDenomPlugin):
    name = '100 - Divide(Sum(Argument 1), Sum(Argument 2))'
    def process(self):
        result = super(OneMinusNumDenomPlugin,self).process() 
        if result is not None:
            return self.output_type(100 - result.get_values())
        return result

register.register('process','Unweighted operations','num_denom',NumDenomPlugin)
register.register('process','Unweighted operations','one_minus_num_denom',OneMinusNumDenomPlugin)
