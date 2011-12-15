from collections import namedtuple
from register import register
from types import Vector, Scalar, Value

class PluginError(Exception):
    pass


class QuestionValidationPlugin(object):
    pass

class QuestionWidget(object):
    pass

class ProcessPlugin(object):
    """ A plugin to process input data """
    name = "Dummy plugin"
    argument_list = ['a','b']
    input_type = None
    output_type = None

    def __init__(self, operation, responsesets):
        self.operation, self.responsesets  = operation, responsesets
        if isinstance(self.input_type, Value)  or isinstance(self.output_type, Value):
            raise PluginError("Plugin is missing input or output type")

    def get_arguments(self):
        if not getattr(self,'_arguments',None):
            ArgumentTuple = namedtuple('ArgumentTuple',self.argument_list)
            arguments = []
            for argument in self.operation.get_arguments():
                arg = argument.get_data(self.responsesets)
                arguments.append(arg)
            self._arguments = ArgumentTuple(*arguments)
        return self._arguments

    def process(self):
        raise NotImplementedError 

    def num_arguments(self):
        return 2

class DataExtractorPlugin(object):
    def get_value(self):
        raise NotImplementedError
