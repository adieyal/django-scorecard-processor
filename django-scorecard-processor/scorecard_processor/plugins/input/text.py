from django.forms import CharField, Textarea
from scorecard_processor.plugins import base, register

class TextBoxField(CharField):
    widget = Textarea
    name = "Long text field"

    def widget_attrs(self, *args, **kwargs):
        attrs = super(TextBoxField,self).widget_attrs(*args, **kwargs)
        if not attrs:
            attrs = {}
        attrs['class'] = attrs.get('class','')+' xxlarge'
        if 'rows' not in attrs:
            attrs['rows'] = 3
        return attrs
            

class TextField(CharField):
    name = "Short text field"

register.register('input','Text field','text', TextField)
register.register('input','Text field','textbox', TextBoxField)
