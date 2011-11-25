from django.forms import IntegerField
from django.forms.util import flatatt
from django.utils.safestring import mark_safe
from django.utils.encoding import StrAndUnicode, force_unicode

from scorecard_processor.plugins import base, register


class Integer(IntegerField):
    name = "Integer"

register.register('input','Number','integer', Integer)
