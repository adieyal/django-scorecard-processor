from django.utils import simplejson
from ierg_results.management.commands.indicator_1_3 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.3.1'
    QUESTION = 'Maternal death is a notifiable event'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 2
        value_column = xrange(4, 7)

        value[column_names[rating_column]] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

