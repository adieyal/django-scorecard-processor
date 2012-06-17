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
        value_column = xrange(2, 5)

        value[column_names[rating_column]] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

