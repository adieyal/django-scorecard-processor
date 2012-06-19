from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '1.3MaternalDeathReviews'
    SURVEY_NAME = 'Maternal Death Reviews'
    COLUM_NAME_ROW_STRING = "A6:V6"
    START_LINE = 6

    IDENTIFIER = '1.3'
    QUESTION = 'Maternal death reviews: at least 90% of maternal deaths notified and reviewed'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value

        return simplejson.dumps(value)

