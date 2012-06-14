from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '1.3MaternalDeathReviews'
    SURVEY_NAME = 'Maternal Death Reviews'
    IDENTIFIER = '1.3'
    QUESTION = 'Maternal death reviews: at least 90% of maternal deaths notified and reviewed'
    COLUM_NAME_ROW_STRING = "A6:W6"
    RATING_COLUMN = 2
    START_LINE = 6
    FINISH_LINE = 81


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

