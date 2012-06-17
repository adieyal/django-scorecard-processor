from django.utils import simplejson
from ierg_results.management.commands.indicator_3_1 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '3.1.1'
    QUESTION = 'Policy implemented'


    def get_json(self, sheet, column_names, i):
        value = {}
        value_column = xrange(3, 6)

        for j in value_column:
            value_index = column_names[j].replace('Source 1 and 2', 'Source 2')
            value[value_index] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

