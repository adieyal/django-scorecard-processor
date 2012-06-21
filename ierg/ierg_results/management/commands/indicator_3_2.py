from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '3.2 Web based reporting'
    SURVEY_NAME = 'Web based reporting'
    COLUM_NAME_ROW_STRING = "A4:E4"
    START_LINE = 4

    IDENTIFIER = '3.2'
    QUESTION = 'All districts are part of a national web based system to report health data and receive feedback'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

