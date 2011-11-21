from django.contrib.localflavor.generic.forms import DateField
from django.forms import SelectDateWidget
from scorecard_processor.plugins import base, register

class DateSelectField(DateField):
    widget = SelectDateWidget
    name = "Date selector"

register.register('input','Date field','date', DateSelectField)
