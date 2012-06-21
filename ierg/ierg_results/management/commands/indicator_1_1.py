from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '1.1BirthRegistration'
    SURVEY_NAME = 'Birth Registration'
    COLUM_NAME_ROW_STRING = "A3:H3"
    START_LINE = 3

    IDENTIFIER = '1.1'
    QUESTION = 'Birth registration: at least 75% of births registered'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1
        value_column = xrange(2, 5)
        value_column_2 = xrange(5, 8)

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        for j in value_column_2:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

