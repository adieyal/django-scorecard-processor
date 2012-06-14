from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '6.1 Reviews of health spending'
    SURVEY_NAME = 'Reviews of health spending'
    IDENTIFIER = '6.1'
    QUESTION = 'Reviews of health spending from all financial sources, including spending on RMNCH, are conducted annually as part of broader health sector reviews'
    COLUM_NAME_ROW_STRING = "A4:E4"
    RATING_COLUMN = 1
    VALUE_COLUMNS = xrange(2, 5)
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        for j in self.VALUE_COLUMNS:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

