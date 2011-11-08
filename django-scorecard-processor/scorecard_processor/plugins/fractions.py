import base
from register import register

class NumDenomPlugin(base.Plugin):
    name = 'Fraction'
    def process(self):
        #den = _sum_values([q for q in qs if q.question_number==denomq], selector)
        #num = _sum_values([q for q in qs if q.question_number==numq], selector)

        #if den in [NA_STR, None] or num in [NA_STR, None]:
        #    return den
        #ratio = NA_STR
        #if den > 0: ratio = num / den * 100
        #return ratio
        return []

class OneMinusNumDenomPlugin(NumDenomPlugin):
    name = 'One minus fraction'
    def process(self):
        #ratio = calc_numdenom(qs, agency_or_country, selector, numq, denomq)
        #ratio = 100 - ratio if ratio not in [NA_STR, None] else ratio
        #return ratio
        return []

register('Agency Indicator','num_denom',NumDenomPlugin)
register('Agency Indicator','one_minus_num_denom',OneMinusNumDenomPlugin)
