from django.utils import simplejson
from ierg_results.management.commands.indicator_1_3 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '1.3.4'
    QUESTION = 'National panel to review maternal deaths in place and meeting regularly'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 16

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

