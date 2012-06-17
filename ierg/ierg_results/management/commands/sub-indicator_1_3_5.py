from django.utils import simplejson
from ierg_results.management.commands.indicator_1_3 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.3.5'
    QUESTION = 'Maternal deaths are captured by the national health information system'


    def get_json(self, sheet, column_names, i):
        value = {}
        value_column = xrange(19, 22)

        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

