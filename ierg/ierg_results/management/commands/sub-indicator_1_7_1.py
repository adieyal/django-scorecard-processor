from django.utils import simplejson
from ierg_results.management.commands.indicator_1_7 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.7.1'
    QUESTION = 'CRVS assessment conducted'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 2
        value_column = xrange(3, 6)
        value_column_2 = 11
        value_column_3 = 12

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        value[column_names[value_column_2]] = sheet.cell(row=i, column=value_column_2).value
        value[column_names[value_column_3]] = sheet.cell(row=i, column=value_column_3).value

        return simplejson.dumps(value)

