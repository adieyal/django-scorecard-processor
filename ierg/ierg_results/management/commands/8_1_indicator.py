from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '8.1 Performance report public'
    SURVEY_NAME = 'Performance report public'
    IDENTIFIER = '8.1'
    QUESTION = 'A health sector performance report for the preceding year is available in the public domain'
    COLUM_NAME_ROW_STRING = "A4:I4"
    RATING_COLUMN = 1
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

