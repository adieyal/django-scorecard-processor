from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '2.3 Impact indicators'
    SURVEY_NAME = 'Impact indicators'
    COLUM_NAME_ROW_STRING = "A4:T4"
    START_LINE = 4

    IDENTIFIER = '2.3'
    QUESTION = 'Data for the 3 impact indicators are available based on data collected in the preceding 3 years'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 2

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']

        return simplejson.dumps(value)

