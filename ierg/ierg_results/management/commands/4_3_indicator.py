from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '4.3 RMNCH expenditure'
    SURVEY_NAME = 'RMNCH expenditure'
    IDENTIFIER = '4.3'
    QUESTION = 'RMNCH expenditure per capita is tracked during the two preceding years, by financing source'
    COLUM_NAME_ROW_STRING = "A4:I4"
    RATING_COLUMN = 1
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

