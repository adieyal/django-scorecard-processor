from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '8.1 Performance report public'
    SURVEY_NAME = 'Performance report public'
    COLUM_NAME_ROW_STRING = "A4:I4"
    START_LINE = 4

    IDENTIFIER = '8.1'
    QUESTION = 'A health sector performance report for the preceding year is available in the public domain'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

