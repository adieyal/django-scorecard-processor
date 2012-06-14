from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '2.3 Impact indicators'
    SURVEY_NAME = 'Impact indicators'
    IDENTIFIER = '2.3'
    QUESTION = 'Data for the 3 impact indicators are available based on data collected in the preceding 3 years'
    COLUM_NAME_ROW_STRING = "A4:S4"
    RATING_COLUMN = 1
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

