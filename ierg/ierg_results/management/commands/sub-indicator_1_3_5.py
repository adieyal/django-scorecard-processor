from django.utils import simplejson
from ierg_results.management.commands.indicator_1_3 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.3.5'
    QUESTION = 'Maternal deaths are captured by the national health information system'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 19

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

