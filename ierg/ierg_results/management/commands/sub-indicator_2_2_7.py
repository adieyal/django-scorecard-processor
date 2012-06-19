from django.utils import simplejson
from ierg_results.management.commands.indicator_2_2 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '2.2.7'
    QUESTION = 'DTP-3'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 28
        value_column = xrange(29, 32)

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

