from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '1.7CRVSimprovement'
    SURVEY_NAME = 'CRVS improvement'
    IDENTIFIER = '1.7'
    QUESTION = 'CRVS improvement plan approved by country government in place'
    COLUM_NAME_ROW_STRING = "A4:Q4"
    RATING_COLUMN = 1
    VALUE_COLUMNS = xrange(6, 9)
    VALUE_COLUMNS_2 = 14
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        for j in self.VALUE_COLUMNS:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        value[column_names[self.VALUE_COLUMNS_2]] = sheet.cell(row=i, column=self.VALUE_COLUMNS_2).value
        return simplejson.dumps(value)

