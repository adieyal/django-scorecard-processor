from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '7.1 Reviews of performance'
    SURVEY_NAME = 'Reviews of performance'
    IDENTIFIER = '7.1'
    QUESTION = 'The country has conducted a annual health sector review in the last year'
    COLUM_NAME_ROW_STRING = "A4:P4"
    RATING_COLUMN = 1
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

