from django.utils import simplejson
from ierg_results.management.commands.indicator_3_1 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '3.1.1'
    QUESTION = 'Policy implemented'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 3

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

