from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '1.1BirthRegistration'
    SURVEY_NAME = 'Birth Registration'
    IDENTIFIER = '1.1'
    QUESTION = 'Birth registration: at least 75% of births registered'
    COLUM_NAME_ROW_STRING = "A3:H3"
    START_LINE = 3
    FINISH_LINE = 78


    def get_json(self, sheet, column_names, i):
        value = {}
        for j in column_names:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

