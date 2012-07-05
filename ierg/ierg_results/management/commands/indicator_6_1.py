from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '6.1 Reviews of health spending'
    SURVEY_NAME = 'Reviews of health spending'
    COLUM_NAME_ROW_STRING = "A4:E4"
    START_LINE = 4

    IDENTIFIER = '6.1'
    QUESTION = 'Reviews of health spending from all financial sources, including spending on RMNCH, are conducted annually as part of broader health sector reviews'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

