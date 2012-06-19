from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '4.2 NHA conducted'
    SURVEY_NAME = 'NHA conducted'
    COLUM_NAME_ROW_STRING = "A3:F3"
    START_LINE = 3

    IDENTIFIER = '4.2'
    QUESTION = 'A NHA was conducted/planned in the last/next 2-3 years'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

