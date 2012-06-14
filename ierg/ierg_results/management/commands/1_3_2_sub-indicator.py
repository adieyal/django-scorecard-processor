from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '1.3MaternalDeathReviews'
    SURVEY_NAME = 'Maternal Death Reviews'
    IDENTIFIER = '1.3.2'
    QUESTION = 'Policy and mechanisms are in place to review all maternal deaths'
    COLUM_NAME_ROW_STRING = "A6:W6"
    RATING_COLUMN = 4
    VALUE_COLUMNS = xrange(8, 11)
    VALUE_COLUMNS_2 = xrange(14, 17)
    START_LINE = 6
    FINISH_LINE = 81


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        for j in self.VALUE_COLUMNS:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        for j in self.VALUE_COLUMNS_2:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

