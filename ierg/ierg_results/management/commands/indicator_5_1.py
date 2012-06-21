from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '5.1 Financial reporting system'
    SURVEY_NAME = 'Financial reporting system'
    COLUM_NAME_ROW_STRING = "A4:K4"
    START_LINE = 4

    IDENTIFIER = '5.1'
    QUESTION = 'A country-led reporting system is in place for externally funded expenditure and predictable commitments These include "compacts" or other similar mechanisms'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

