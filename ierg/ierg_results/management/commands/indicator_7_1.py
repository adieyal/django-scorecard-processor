from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '7.1 Reviews of performance'
    SURVEY_NAME = 'Reviews of performance'
    COLUM_NAME_ROW_STRING = "A4:P4"
    START_LINE = 4

    IDENTIFIER = '7.1'
    QUESTION = 'The country has conducted a annual health sector review in the last year'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

