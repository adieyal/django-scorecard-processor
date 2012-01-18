import math
from scorecard_processor.plugins.types import NOT_APPLICABLE

def criterion_absolute(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE: 
        raise CannotCalculateException() 
    if cur_val == None: 
        raise MissingValueException() 

    if math.fabs(cur_val - criterion_param) < 0.000000001:
        return True
    return False

def criterion_relative_increase(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE or base_val == NOT_APPLICABLE:
        raise CannotCalculateException()

    if cur_val == None or base_val == None: 
        raise MissingValueException() 

    if cur_val > base_val * (1 + criterion_param / 100.0):
        return True
    return False

def criterion_relative_decrease(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE or base_val == NOT_APPLICABLE:
        raise CannotCalculateException()
    if cur_val == None or base_val == None: 
        raise MissingValueException() 

    if cur_val < base_val * (1 - criterion_param / 100.0):
        return True
    return False

def criterion_increase(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE or base_val == NOT_APPLICABLE:
        raise CannotCalculateException()
    if cur_val == None or base_val == None: 
        raise MissingValueException() 

    if cur_val > base_val:
        return True
    return False

def criterion_decrease(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE or base_val == NOT_APPLICABLE:
        raise CannotCalculateException()
    if cur_val == None or base_val == None: 
        raise MissingValueException()

    if cur_val < base_val:
        return True
    return False

def criterion_absolute_greater_than(base_val, cur_val, criterion_param):

    if cur_val == NOT_APPLICABLE: 
        raise CannotCalculateException() 
    if cur_val == None: raise MissingValueException()
    if cur_val > criterion_param:
        return True
    return False

def criterion_absolute_less_than(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE: 
        raise CannotCalculateException() 
    if cur_val == None: raise MissingValueException()
    if cur_val < criterion_param:
        return True
    return False

def criterion_absolute_increase(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE or base_val == NOT_APPLICABLE:
        raise CannotCalculateException()
    if cur_val == None or base_val == None: 
        raise MissingValueException()

    if cur_val - criterion_param > base_val:
        return True
    return False

def criterion_absolute_decrease(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE or base_val == NOT_APPLICABLE:
        raise CannotCalculateException()
    if cur_val == None or base_val == None: 
        raise MissingValueException()

    if cur_val + criterion_param < base_val:
        return True
    return False

def criterion_both_yes(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE: 
        raise CannotCalculateException() 
    if cur_val == None or len(cur_val.strip()) != 2:
        raise MissingValueException()

    if cur_val.lower() == "yy":
        return True
    return False

class MissingValueException(Exception):
    pass

class CannotCalculateException(Exception):
    pass

def criterion_first_yes(base_val, cur_val, criterion_param):
    if cur_val == NOT_APPLICABLE: 
        raise CannotCalculateException() 
    if cur_val == None or len(cur_val) == 0:
        raise MissingValueException()

    if cur_val.lower()[0] == "y":
        return True
    return False


indicators = {
     u'1DP': {'arrow_function': u'Absolute greater than x%',
              'arrow_value': 0.01,
              'tick_function': u'Absolute % Target',
              'tick_value': 100.0},
     u'2DPa': {'arrow_function': u'Decrease relative to baseline (no minimum)',
               'arrow_value': None,
               'tick_function': u'Minimum x% Decrease relative to baseline',
               'tick_value': 49.5},
     u'2DPb': {'arrow_function': u'Increase relative to baseline (no minimum)',
               'arrow_value': None,
               'tick_function': u'Absolute greater than x%',
               'tick_value': 49.5},
     u'2DPc': {'arrow_function': u'Increase relative to baseline (no minimum)',
               'arrow_value': None,
               'tick_function': u'Absolute greater than x%',
               'tick_value': 65.5},
     u'3DP': {'arrow_function': u'Increase relative to baseline (no minimum)',
              'arrow_value': None,
              'tick_function': u'Absolute greater than x%',
              'tick_value': 89.5},
     u'4DP': {'arrow_function': u'Increase relative to baseline (no minimum)',
              'arrow_value': None,
              'tick_function': u'Absolute greater than x%',
              'tick_value': 89.5},
     u'5DPa': {'arrow_function': u'Decrease relative to baseline (no minimum)',
               'arrow_value': None,
               'tick_function': u'Minimum x% Decrease relative to baseline',
               'tick_value': 32.5},
     u'5DPb': {'arrow_function': u'Decrease relative to baseline (no minimum)',
               'arrow_value': None,
               'tick_function': u'Minimum x% Decrease relative to baseline',
               'tick_value': 32.5},
     u'5DPc': {'arrow_function': u'Decrease relative to baseline (no minimum)',
               'arrow_value': None,
               'tick_function': u'Minimum x% Decrease relative to baseline',
               'tick_value': 65.5},
     u'6DP': {'arrow_function': u'Absolute greater than x%',
              'arrow_value': 0.01,
              'tick_function': u'Absolute % Target',
              'tick_value': 100.0},
     u'7DP': {'arrow_function': u'Absolute greater than x%',
              'arrow_value': 0.01,
              'tick_function': u'Absolute % Target',
              'tick_value': 100.0},
     u'8DP': {'arrow_function': u'Absolute greater than x%',
              'arrow_value': 0.01,
              'tick_function': u'Absolute % Target',
              'tick_value': 100.0}
    }


criteria_funcs = {
   "Absolute % Target" : criterion_absolute,
   "Minimum x% Increase relative to baseline" : criterion_relative_increase,
   "Minimum x% Decrease relative to baseline" : criterion_relative_decrease,
   "Increase relative to baseline (no minimum)" : criterion_increase,
   "Decrease relative to baseline (no minimum)" : criterion_decrease,
   "Absolute greater than x%" : criterion_absolute_greater_than,
   "Absolute less than x%" : criterion_absolute_less_than,
   "Absolute Value Increase" : criterion_absolute_increase,
   "Absolute Value Decrease" : criterion_absolute_decrease,
   "Both Questions Yes" : criterion_both_yes,
   "First Question Yes" : criterion_first_yes,
}
