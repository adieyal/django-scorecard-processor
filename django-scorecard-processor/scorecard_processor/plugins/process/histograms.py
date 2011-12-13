from scorecard_processor.plugins import base, register

class Count(base.ProcessPlugin):
    name = 'Count'
    argument_list = ['items']
    input_type = base.Vector
    output_type = base.Scalar

    def process(self):
        values = self.get_arguments().items.get_values()
        return self.output_type(len(values))

class CountValue(Count):
    key = 'yes'
    name = "Frequency of keyword (%)"
    def process(self):
        items = self.get_arguments().items.get_values()
        count = len(items)
        if count == 0:
            return None
        count_values = len(filter(lambda x: x.get_value().lower() == self.key,items))
        return self.output_type(count_values / count * 100)


register.register('process','Count','count_items',Count)
register.register('process','Count','keyword_frequency',CountValue)
