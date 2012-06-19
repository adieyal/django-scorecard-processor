from django.utils import simplejson
from ierg_results.management.commands.indicator_1_3 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.3.2'
    QUESTION = 'Policy and mechanisms are in place to review all maternal deaths'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 3
        value_column = xrange(7, 10)
        value_column_2 = xrange(13, 16)

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        for j in value_column_2:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

