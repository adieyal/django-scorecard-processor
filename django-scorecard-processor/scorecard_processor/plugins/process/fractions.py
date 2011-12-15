from scorecard_processor.plugins import base, register
from collections import namedtuple
import decimal

def sum_values(x, y):
    return x + y

class NumDenomPlugin(base.ProcessPlugin):
    name = 'Divide(Sum(Argument 1), Sum(Argument 2))'
    argument_list = ['numerator', 'denominator']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        """ First test if the arguments come from the same survey, if they do,
        pair responses together, and filter out if it is missing
        numerator/denominator """
        arg1, arg2 = self.operation.get_arguments()
        
        try:
            pair_values = arg1.instance.survey_id == arg2.instance.survey_id
        except AttributeError:
            pair_values = False

        numerator = []
        denominator = []

        if pair_values:
            filter_responses = {}
            for response in self.get_arguments().numerator.get_values():
                filter_responses[response.response_set_id] = filter_responses.get(response.response_set_id,{})
                filter_responses[response.response_set_id]['num'] = response.get_value()

            for response in self.get_arguments().denominator.get_values():
                if response.response_set_id in filter_responses:
                    filter_responses[response.response_set_id]['denom'] = response.get_value()
            
            for frac in filter_responses.values():
                if 'num' in frac and 'denom' in frac:
                    numerator.append(float(frac['num']))
                    denominator.append(float(frac['denom']))
        else:
            numerator = [float(x.get_value()) for x in self.get_arguments().numerator.get_values()]
            denominator = [float(x.get_value()) for x in self.get_arguments().denominator.get_values()]

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
