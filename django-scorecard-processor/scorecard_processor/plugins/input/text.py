from django.forms import CharField, Textarea
from scorecard_processor.plugins import base, register

class TextBoxField(CharField):
    widget = Textarea

register.register('input','Long text field','text',CharField)
register.register('input','Long text field','textbox',TextBoxField)
