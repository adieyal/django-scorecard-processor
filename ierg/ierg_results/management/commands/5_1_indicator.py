from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '5.1 Financial reporting system'
    SURVEY_NAME = 'Financial reporting system'
    IDENTIFIER = '5.1'
    QUESTION = 'A country-led reporting system is in place for externally funded expenditure and predictable commitments These include "compacts" or other similar mechanisms'
    COLUM_NAME_ROW_STRING = "A4:K4"
    RATING_COLUMN = 1
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

