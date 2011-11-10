from collections import namedtuple
from register import register


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

    def get_scorecard_arguments(self, response_instance):
        #TODO: make more generic, not specific to scorecards
        #TODO: more efficient queries
        values = []
        for argument in self.operationargument_set.all(): 
            values += response_instance.response_set.get(question = argument.instance)
            
        return self.ArgumentTuple(values)

    def process(self):
        raise NotImplementedError 

    def process_item(self, arguments):
        # Takes and instance of self.ArgumentTuple
        raise NotImplementedError 

    def num_arguments(self):
        return 2

class DataExtractorPlugin:
    pass
