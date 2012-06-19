from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '3.1 eHealth strategy'
    SURVEY_NAME = 'eHealth strategy'
    COLUM_NAME_ROW_STRING = "A4:I4"
    START_LINE = 4

    IDENTIFIER = '3.1'
    QUESTION = 'National eHealth strategy and plan is in place'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

