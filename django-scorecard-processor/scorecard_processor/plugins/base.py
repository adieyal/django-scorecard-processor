from collections import namedtuple
from register import register

VECTOR = 'vector'
SCALAR = 'scalar'

class PluginError(Exception):
    pass

class Value(object):
    def __init__(self, item, extractor_class=None):
        if extractor_class:
            self.value = self.extractor_class(item)
        else:
            self.value = item

    def __repr__(self):
        return repr(self.value)

    def __unicode__(self):
        return unicode(self.value)

    def get_value(self):
        try:
            return self.value.get_value()
        except AttributeError:
            return self.value

    def get_values(self):
        try:
            return self.value.get_value()
        except AttributeError:
            return self.value

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
        if self.input_type not in (VECTOR,SCALAR) or self.output_type not in (VECTOR, SCALAR):
            raise PluginError("Plugin is missing input or output type")

    def get_arguments(self):
        if not getattr(self,'_arguments',None):
            ArgumentTuple = namedtuple('ArgumentTuple',self.argument_list)
            arguments = []
            for argument in self.operation.operationargument_set.all():
                arguments.append(Value(argument.get_values(self.responsesets)))
            self._arguments = ArgumentTuple(*arguments)
        return self._arguments

    def process(self):
        raise NotImplementedError 

    def num_arguments(self):
        return 2

class DataExtractorPlugin(object):
    def get_value(self):
        raise NotImplementedError
