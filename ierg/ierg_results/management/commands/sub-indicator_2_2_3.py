from django.utils import simplejson
from ierg_results.management.commands.indicator_2_2 import Command as Indicator


class Command(Indicator):
    IDENTIFIER = '2.2.3'
    QUESTION = 'Antiretroviral prophylaxis for PMTCT'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 12
        value_column = xrange(13, 16)

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

