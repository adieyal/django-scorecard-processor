from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '1.5COD'
    SURVEY_NAME = 'COD'
    COLUM_NAME_ROW_STRING = "A3:E3"
    START_LINE = 3

    IDENTIFIER = '1.5'
    QUESTION = 'Coverage of registration: cause of death > 60%'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1
        value_column = xrange(2, 5)

        value[column_names[rating_column]] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

