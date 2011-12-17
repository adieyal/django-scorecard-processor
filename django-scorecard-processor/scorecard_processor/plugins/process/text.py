from scorecard_processor.plugins import base, register

def sum_values(x, y):
    return x + y

class TextRenderer(base.Scalar):
    def get_value(self):
        return "\n\n".join([i[1] for i in self.value])

    def _as_html(self):
        if not self.value:
            return ''
        row = "<dt>%s</dt><dd>%s</dd>"
        return "<dl class='concat'>%s</dl>" % ''.join([row % i for i in self.value])

        

class Concat(base.ProcessPlugin):
    name = 'Concatenate responses'
    argument_list = ['response']
    input_type = base.Vector
    output_type = TextRenderer
    allow_cache = False

    def process(self):
        return self.output_type([(v.response_set.entity, v.get_value()) for v in self.get_arguments().response.get_values()])

register.register('process','Text','concat',Concat)
