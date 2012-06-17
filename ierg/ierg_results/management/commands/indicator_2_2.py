from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '2.2 Coverage indicators'
    SURVEY_NAME = 'Coverage indicators'
    COLUM_NAME_ROW_STRING = "A4:AJ4"
    START_LINE = 4

    IDENTIFIER = '2.2'
    QUESTION = 'Overall- 8 indicators from 2010 - 2012'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 2
        value_column = [4, 8, 12, 16, 20, 24, 28, 32]

        value[column_names[rating_column]] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

