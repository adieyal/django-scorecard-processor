from django.utils import simplejson
from ierg_results.management.commands.indicator_1_3 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.3.3'
    QUESTION = 'National panel to review maternal deaths in place'


    def get_json(self, sheet, column_names, i):
        value = {}
        value_column = xrange(10, 13)

        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

