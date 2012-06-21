from django.utils import simplejson
from ierg_results.management.commands.indicator_2_2 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '2.2.8'
    QUESTION = 'Antibiotic treatment for pneumonia'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 32
        value_column = xrange(33, 36)

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

