from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '1.6QoC'
    SURVEY_NAME = 'QoC'
    COLUM_NAME_ROW_STRING = "A3:E3"
    START_LINE = 3

    IDENTIFIER = '1.6'
    QUESTION = 'Quality of care assessment conducted (SPA, EMOC)'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1
        value_column = xrange(2, 5)

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

