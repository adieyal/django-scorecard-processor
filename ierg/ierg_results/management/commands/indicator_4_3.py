from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '4.3 RMNCH expenditure'
    SURVEY_NAME = 'RMNCH expenditure'
    COLUM_NAME_ROW_STRING = "A4:I4"
    START_LINE = 4

    IDENTIFIER = '4.3'
    QUESTION = 'RMNCH expenditure per capita is tracked during the two preceding years, by financing source'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

