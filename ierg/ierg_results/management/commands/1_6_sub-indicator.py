from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '1.5QoC'
    SURVEY_NAME = 'QoC'
    IDENTIFIER = '1.6'
    QUESTION = 'Quality of care assessment conducted (SPA, EMOC)'
    COLUM_NAME_ROW_STRING = "A3:E3"
    RATING_COLUMN = 1
    VALUE_COLUMNS = xrange(2, 5)
    START_LINE = 3
    FINISH_LINE = 78


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        for j in self.VALUE_COLUMNS:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

