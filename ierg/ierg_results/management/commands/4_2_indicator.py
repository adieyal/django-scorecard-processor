from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '4.2 NHA conducted'
    SURVEY_NAME = 'NHA conducted'
    IDENTIFIER = '4.2'
    QUESTION = 'A NHA was conducted/planned in the last/next 2-3 years'
    COLUM_NAME_ROW_STRING = "A3:F3"
    RATING_COLUMN = 1
    START_LINE = 3
    FINISH_LINE = 78


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

