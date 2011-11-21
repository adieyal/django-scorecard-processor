from django.forms import CharField, Textarea
from scorecard_processor.plugins import base, register

class TextBoxField(CharField):
    widget = Textarea
    name = "Long text field"

class TextField(CharField):
    name = "Short text field"

register.register('input','Text field','text', TextField)
register.register('input','Text field','textbox', TextBoxField)
