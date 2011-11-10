from collections import namedtuple
from register import register

class Value:
    def __init__(self, item, extractor_class=None):
        if extractor_class:
            self.value = self.extractor_class(item)
        else:
            self.value = item

    def get_value():
        try:
            return self.value.get_value()
        except AttributeError:
            return self.value

class QuestionValidationPlugin:
    pass

class QuestionWidget:
    pass

class ProcessPlugin:
    """ A plugin to process input data """
    name = "Dummy plugin"
    argument_list = ['a','b']

    def __init__(self, operation):
        self.operation = operation
        if self.operation.operationargument_set.count() == self.num_arguments:
            self.ArgumentTuple = namedtuple('ArgumentTuple',self.argument_list)

    def process(self):
        raise NotImplementedError 

    def num_arguments(self):
        return 2

class DataExtractorPlugin:
    def get_value(self):
        raise NotImplementedError
