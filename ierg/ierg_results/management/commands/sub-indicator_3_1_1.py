from django.utils import simplejson
from ierg_results.management.commands.indicator_3_1 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '3.1.1'
    QUESTION = 'Policy implemented'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 2

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

