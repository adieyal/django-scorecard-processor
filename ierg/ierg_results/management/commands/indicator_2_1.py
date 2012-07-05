from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '2.1 Health_info'
    SURVEY_NAME = 'Health info'
    COLUM_NAME_ROW_STRING = "A4:J4"
    START_LINE = 4

    IDENTIFIER = '2.1'
    QUESTION = 'Health indicators additional information'


    def get_json(self, sheet, column_names, i):
        value = {}

        return simplejson.dumps(value)

