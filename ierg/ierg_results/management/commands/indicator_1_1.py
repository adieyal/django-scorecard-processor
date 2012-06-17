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

        for j in column_names:
            value[column_names[j]] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

